
import redis
import csv
import requests
# from flask import Flask
import faker


def login_users(n):

    with open('tokens.csv', 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(["user_id", "token", "account_id"])
        for i in range(1, n + 1):
            print(i, end=" ")
            res = requests.post("http://tguio.club:8848/api/auth/signin", json={
                "username": "user"+str(i + 10010),
                "password": "000000"
            })
            content = res.json()
            if content["code"] == 200:
                token = content["content"]["token"]
                user_id = content["content"]["user_id"]
                account_id = content["content"]["account_id"][0]
                spamwriter.writerow([user_id, token, account_id])


def clear_redis():

    r = redis.StrictRedis(host='tguio.club', port=6379,
                          db=0, password="Aa1@0000")
    r.flushall()


def admin_login(username):
    res = requests.post("http://tguio.club:8848/api/auth/signin", json={
        "username": username,
        "password": "000000"
    })
    res = res.json()
    print(res)
    return res["content"]["token"]


def create_new_activity(token):
    res = requests.post("http://tguio.club:8848/api/loan/",
                        headers={
                            "Authorization": token
                        },
                        json={
                            "activity_apr": 1.0,
                            "activity_endTime": "2008-12-12 23:12:1",
                            "activity_initMoney": 10,
                            "activity_moneyLimit": 10000000,
                            "activity_name": "adwa",
                            "activity_replayTime": 10,
                            "activity_startTime": "2008-12-12 23:12:1",
                            "activity_timeLimit": "3/6",

                            "activity_totalAmount": 10 * 10000 * 1,

                            "activity_totalQuantity": 10000,
                            "activity_perPrice": 100,
                            "activity_oneMaxAmount": 1,

                            "rule": {
                                "activity_ageFloor": 0,
                                "activity_ageUp": 100,
                                "activity_checkDishonest": False,
                                "activity_checkNation": True,
                                "activity_checkOverdual": True,
                                "activity_checkwork": True,
                                "activity_guarantee": True,
                                "activity_pledge": True
                            }
                        })

    res = res.json()
    print(res)
    activity_id = res["content"]["activity_id"]
    return activity_id


if __name__ == "__main__":
    # app = Flask("name")

    # @app.route('/hello')
    # def hello():
    #     return {
    #         "activity_id": newid
    #     }
    # app.run()

    print("start...")
    # clear_redis()
    # login_users(10)
    newid = create_new_activity(admin_login("user10005"))
    print(newid)
