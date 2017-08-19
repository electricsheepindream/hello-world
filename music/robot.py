from werobot import WeRoBot


robot = WeRoBot(enable_session=False,
                token='esid',
                APP_ID='wxc6ec8eda771e9cf2',
                APP_SECRET='99e8d052e83864de0df9c973382b5ffd'
                )


@robot.handler
def hello(message):
    return '傻瓜'
