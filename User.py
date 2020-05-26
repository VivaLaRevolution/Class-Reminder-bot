import discord

class User:
    def __init__(self, member, roles, nick):
        self.member = member
        self.roles = roles
        self.nick = nick
        self.remind = True
        

    def isRemind(self,boolean):
        self.remind = boolean

    async def addRole(self,role):
        if role not in self.roles:
                await self.member.add_roles(self.member, role)
        

    
