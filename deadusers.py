#!/usr/bin/env python3
import datetime
import sys
from datetime import datetime, timedelta, timezone

import boto3
from tabulate import tabulate


if __name__ == "__main__":
    now = datetime.now(timezone.utc)
    days30 = now - timedelta(days=30)
    
    iam = boto3.client("iam")
    users = {
        username: {
            "PasswordLastUsed": iam.get_user(UserName=username)["User"].get("PasswordLastUsed", None),
            "AccessKeys": [
                {
                    "AccessKeyId": access_key_id,
                    "LastUsed": iam.get_access_key_last_used(AccessKeyId=access_key_id)["AccessKeyLastUsed"].get("LastUsedDate", None)
                }
                for list_access_keys_page in iam.get_paginator("list_access_keys").paginate(UserName=username)
                for access_key in list_access_keys_page["AccessKeyMetadata"]
                for access_key_id in [access_key["AccessKeyId"]]
            ]

        }
        for list_users_page in iam.get_paginator("list_users").paginate()
        for user in list_users_page["Users"]
        for username in [user["UserName"]]
    }

    dead_users = {}
    for username, userdata in users.items():
        last_used = userdata["PasswordLastUsed"]
        reasons = []
        if last_used is None:
            reasons.append(f"Never logged in on console")
        elif last_used < days30:
            days_ago = (now - last_used).days
            reasons.append(f"Last console login: {last_used} ({days_ago} days ago)")
        for access_key in userdata["AccessKeys"]:
            last_used = access_key["LastUsed"]
            if last_used is None:
               reasons.append(f"Access key {access_key['AccessKeyId']} never used")
            elif last_used < days30:
                days_ago = (now - last_used).days
                reasons.append(f"Access key {access_key['AccessKeyId']} last used: {last_used} ({days_ago} days ago)")
        if reasons:
            dead_users[username] = reasons

    table = [
        [username, "\n".join(reasons)]
        for username, reasons in dead_users.items()
    ]
    table_headers = ("User", "Reason(s)")
    print(tabulate(table, headers=table_headers, tablefmt="grid"))
