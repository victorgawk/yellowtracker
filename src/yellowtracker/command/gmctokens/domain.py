import enum
import discord

__all__ = (
    'GmcToken',
    'GmcBox',
    'GmcBoxReq',
    'GmcTokenAccAmount',
    'GmcTokenAcc',
    'GmcTokenUser',
)

class GmcToken(enum.Enum):
    SEIREN = "Seiren"
    SUSHI = "Sushi"
    BLACKTALON = "BlackTalon"
    BOREAS = "Boreas"
    MUUI = "Muui"
    SHIRIS = "Shiris"
    HOWL = "Howl"
    GEMINI = "Gemini"
    LANCE = "Lance"
    SAEN = "Saen"

class GmcBox(enum.Enum):
    CRIMSON = "Crimson"
    CERULEAN = "Cerulean"
    SAFFRON = "Saffron"

class GmcBoxReq:
    def __init__(self, id: int, box: GmcBox, tokens: list[GmcToken]):
        self.id = id
        self.box = box
        self.tokens = tokens

class GmcTokenAccAmount:
    def __init__(self, token: GmcToken, amount: int):
        self.token = token
        self.amount = amount

class GmcTokenAcc:
    def __init__(self, id: int = None):
        self.id = id
        self.amounts: dict[GmcToken, GmcTokenAccAmount] = {}
        self.boxReqs: dict[GmcBox, GmcBoxReq] = {}

class GmcTokenUser:
    def __init__(self, bot, user: discord.User):
        self.bot = bot
        self.user = user
        self.accs: list[GmcTokenAcc] = None

    async def initAccs(self):
        self.accs = await self.repoGetGmcTokenAccs(self.user)

    @staticmethod
    def mock():
        gmcTokenUser = GmcTokenUser(None, None)
        gmcTokenAccount = GmcTokenAcc()
        gmcTokenUser.accs.append(gmcTokenAccount)
        gmcTokenAccount.amounts[GmcToken.SEIREN] = GmcTokenAccAmount(GmcToken.SEIREN, 5)
        gmcTokenAccount.amounts[GmcToken.BOREAS] = GmcTokenAccAmount(GmcToken.BOREAS, 2)
        gmcTokenAccount.amounts[GmcToken.SUSHI] = GmcTokenAccAmount(GmcToken.SUSHI, 2)
        gmcTokenAccount.amounts[GmcToken.MUUI] = GmcTokenAccAmount(GmcToken.MUUI, 2)
        gmcTokenAccount.amounts[GmcToken.HOWL] = GmcTokenAccAmount(GmcToken.HOWL, 2)
        return gmcTokenUser

    def embed(self):
        embed = discord.Embed(color=discord.Colour.gold(), title="GMC Tokens")
        tokens = ""
        for gmcToken in GmcToken:
            tokens += f"{gmcToken.value}\n"
        embed.add_field(name="Token / Acc", value=tokens, inline=True)

        if len(self.accs) > 0:
            accs_title = ""
            for accId in range(len(self.accs)):
                if accId > 0:
                    accs_title += " | "
                accs_title += f"{accId + 1}"
            accsStr = ""
            for gmcToken in GmcToken:
                row = ""
                for accId in range(len(self.accs)):
                    req_per_token = self.get_req_per_token(accId)
                    gmcTokenAccount = self.accs[accId]
                    if len(row) > 0:
                        row += " | "
                    gmcTokenAmounts = gmcTokenAccount.amounts
                    tokenAmnt = 0
                    if gmcTokenAmounts.get(gmcToken) is not None:
                        tokenAmnt = gmcTokenAmounts[gmcToken].amount
                    if req_per_token.get(gmcToken) is not None:
                        if req_per_token.get(gmcToken) > 0:
                            tokenAmnt = f"**{tokenAmnt}**"
                    row += f"{tokenAmnt}"
                accsStr += f"{row}\n"
            embed.add_field(name=accs_title, value=accsStr, inline=True)
            embed.set_footer(text = "Bold values indicate that you need one or more tokens to claim a box")

            boxesStr = ""
            for accId in range(len(self.accs)):
                boxesStr += f"Acc {accId + 1}:"
                box_names = self.get_claimable_box_names(accId)
                for box_name in box_names:
                    boxesStr += f" 🎁 {box_name}"
                boxesStr += "\n"
            embed.add_field(name="Claimable Boxes", value=boxesStr, inline=False)

        return embed

    def get_token_amount(self, accId: int, gmcToken: GmcToken) -> int:
        gmcTokenAmount = self.accs[accId].amounts.get(gmcToken)
        if gmcTokenAmount is None:
            return 0
        else:
            return gmcTokenAmount.amount

    def get_tokens_req(self, accId: int, gmcBox: GmcBox):
        boxReq = self.accs[accId].boxReqs.get(gmcBox)
        if boxReq is None:
            return []
        else:
            return boxReq.tokens

    def get_req_per_token(self, accId) -> dict[GmcToken, int]:
        acc = self.accs[accId]
        req_per_token = {}
        for box in acc.boxReqs:
            for token in acc.boxReqs[box].tokens:
                currVal = req_per_token.get(token)
                if currVal is None:
                    currVal = 0
                req_per_token[token] = currVal + 2
        for token in acc.amounts:
            if req_per_token.get(token) is not None:
                req_per_token[token] -= acc.amounts[token].amount
        return req_per_token

    def get_claimable_box_names(self, accId: int) -> list[str]:
        acc = self.accs[accId]
        claimable_box_names = []
        if self.is_normal_box_claimable(accId):
            claimable_box_names.append("Normal")
        for box in acc.boxReqs:
            is_claimable = False
            if len(acc.boxReqs[box].tokens) > 0:
                is_claimable = True
                for token in acc.boxReqs[box].tokens:
                    amnt = 0
                    if acc.amounts.get(token) is not None:
                        amnt = acc.amounts[token].amount
                    if amnt < 2:
                        is_claimable = False
                        break
            if is_claimable:
                claimable_box_names.append(box.value)
        return claimable_box_names

    async def add_account(self) -> None:
        acc = GmcTokenAcc()
        await self.repoCreateAcc(acc)
        self.accs.append(acc)

    async def set_token_amount(self, accId: int, gmcToken: GmcToken, amount: int) -> None:
        amount = GmcTokenAccAmount(gmcToken, amount)
        await self.repoSaveAccAmount(accId, amount)
        self.accs[accId].amounts[gmcToken] = amount

    async def delete_account(self, accId: int) -> None:
        await self.repoDeleteAcc(accId)
        del self.accs[accId]

    async def set_box_requirements(self, accId: int, gmcBox: GmcBox, gmcTokens: list[GmcToken]) -> None:
        gmcBoxReq = self.accs[accId].boxReqs.get(gmcBox)
        if gmcBoxReq is None:
            gmcBoxReq = GmcBoxReq(None, gmcBox, [])
        gmcBoxReq.tokens = gmcTokens
        self.accs[accId].boxReqs[gmcBox] = gmcBoxReq
        await self.repoSaveGmcBoxReq(accId, gmcBoxReq)

    def is_normal_box_claimable(self, accId: int) -> bool:
        acc = self.accs[accId]
        normalBoxTokens = [GmcToken.SEIREN, GmcToken.BOREAS, GmcToken.SUSHI, GmcToken.MUUI, GmcToken.HOWL, GmcToken.BLACKTALON, GmcToken.SHIRIS]
        for token in normalBoxTokens:
            amount = acc.amounts.get(token)
            if amount is None or acc.amounts[token].amount < 1:
                return False
        return True

    async def claim_normal_box(self, accId: int) -> None:
        acc = self.accs[accId]
        normalBoxTokens = [GmcToken.SEIREN, GmcToken.BOREAS, GmcToken.SUSHI, GmcToken.MUUI, GmcToken.HOWL, GmcToken.BLACKTALON, GmcToken.SHIRIS]
        for token in normalBoxTokens:
            acc.amounts[token].amount -= 1
            await self.repoSaveAccAmount(accId, acc.amounts[token])

    async def claim_box(self, accId: int, gmcBox: GmcBox) -> None:
        acc = self.accs[accId]
        gmcBoxReq = acc.boxReqs[gmcBox]
        for token in gmcBoxReq.tokens:
            acc.amounts[token].amount -= 2
            await self.repoSaveAccAmount(accId, acc.amounts[token])
        await self.repoDeleteGmcBoxReq(gmcBoxReq)
        acc.boxReqs[gmcBox].tokens = []

    async def repoGetGmcTokenAccs(self, user: discord.User) -> list[GmcTokenAcc]:
        accs = []
        conn = await self.bot.pool_acquire()
        try:
            sql = "SELECT id FROM gmc_token_acc WHERE id_user = $1 ORDER BY id ASC"
            accsDb = await conn.fetch(sql, user.id)
            for accDb in accsDb:
                acc = GmcTokenAcc(accDb['id'])
                sql = "SELECT token_name, amount FROM gmc_token_acc_amount WHERE id_gmc_token_acc = $1"
                amountsDb = await conn.fetch(sql, acc.id)
                for amountDb in amountsDb:
                    amount = GmcTokenAccAmount(GmcToken(amountDb['token_name']), amountDb['amount'])
                    acc.amounts[amount.token] = amount
                sql = "SELECT id, box_name FROM gmc_token_box_req WHERE id_gmc_token_acc = $1"
                boxReqsDb = await conn.fetch(sql, acc.id)
                for boxReqDb in boxReqsDb:
                    boxReq = GmcBoxReq(boxReqDb['id'], GmcBox(boxReqDb['box_name']), [])
                    sql = "SELECT token_name FROM gmc_token_box_req_token WHERE id_gmc_token_box_req = $1"
                    boxReqTokensDb = await conn.fetch(sql, boxReq.id)
                    for boxReqTokenDb in boxReqTokensDb:
                        token = GmcToken(boxReqTokenDb['token_name'])
                        boxReq.tokens.append(token)
                    acc.boxReqs[boxReq.box] = boxReq
                accs.append(acc)
        finally:
            await self.bot.pool_release(conn)
        return accs

    async def repoCreateAcc(self, acc: GmcTokenAcc) -> None:
        conn = await self.bot.pool_acquire()
        try:
            sql = "SELECT nextval('gmc_token_acc_seq') AS x"
            seq = await conn.fetchrow(sql)
            acc.id = seq['x']
            sql = "INSERT INTO gmc_token_acc(id, id_user) VALUES ($1, $2)"
            await conn.execute(sql, acc.id, self.user.id)
        finally:
            await self.bot.pool_release(conn)

    async def repoSaveAccAmount(self, accId: int, accAmount: GmcTokenAccAmount) -> None:
        acc = self.accs[accId]
        conn = await self.bot.pool_acquire()
        try:
            sql = "SELECT FROM gmc_token_acc_amount WHERE id_gmc_token_acc = $1 AND token_name = $2"
            accDb = await conn.fetchrow(sql, acc.id, accAmount.token.value)
            sql = "INSERT INTO gmc_token_acc_amount(id_gmc_token_acc, token_name, amount) VALUES ($1, $2, $3)"
            if accDb is not None:
                sql = "UPDATE gmc_token_acc_amount SET amount = $3 WHERE id_gmc_token_acc = $1 AND token_name = $2"
            await conn.execute(sql, acc.id, accAmount.token.value, accAmount.amount)
        finally:
            await self.bot.pool_release(conn)

    async def repoDeleteAcc(self, accId: int) -> None:
        acc = self.accs[accId]
        conn = await self.bot.pool_acquire()
        try:
            sql = "DELETE FROM gmc_token_box_req_token WHERE id_gmc_token_box_req IN (SELECT id FROM gmc_token_box_req WHERE id_gmc_token_acc = $1)"
            await conn.execute(sql, acc.id)
            sql = "DELETE FROM gmc_token_box_req WHERE id_gmc_token_acc = $1"
            await conn.execute(sql, acc.id)
            sql = "DELETE FROM gmc_token_acc_amount WHERE id_gmc_token_acc = $1"
            await conn.execute(sql, acc.id)
            sql = "DELETE FROM gmc_token_acc WHERE id = $1"
            await conn.execute(sql, acc.id)
        finally:
            await self.bot.pool_release(conn)

    async def repoSaveGmcBoxReq(self, accId: int, gmcBoxReq: GmcBoxReq) -> None:
        acc = self.accs[accId]
        conn = await self.bot.pool_acquire()
        try:
            if gmcBoxReq.id is None:
                sql = "SELECT nextval('gmc_token_box_req_seq') AS x"
                seq = await conn.fetchrow(sql)
                gmcBoxReq.id = seq['x']
                sql = "INSERT INTO gmc_token_box_req(id, id_gmc_token_acc, box_name) VALUES ($1, $2, $3)"
                await conn.execute(sql, gmcBoxReq.id, acc.id, gmcBoxReq.box.value)
            sql = "SELECT token_name FROM gmc_token_box_req_token WHERE id_gmc_token_box_req = $1"
            tokensDb = [GmcToken(x["token_name"]) for x in await conn.fetch(sql, gmcBoxReq.id)]
            for tokenDb in tokensDb:
                if tokenDb not in gmcBoxReq.tokens:
                    sql = "DELETE FROM gmc_token_box_req_token WHERE id_gmc_token_box_req = $1 AND token_name = $2"
                    await conn.execute(sql, gmcBoxReq.id, tokenDb.value)
            for token in gmcBoxReq.tokens:
                if token not in tokensDb:
                    sql = "INSERT INTO gmc_token_box_req_token(id_gmc_token_box_req, token_name) VALUES ($1, $2)"
                    await conn.execute(sql, gmcBoxReq.id, token.value)
        finally:
            await self.bot.pool_release(conn)

    async def repoDeleteGmcBoxReq(self, gmcBoxReq: GmcBoxReq) -> None:
        conn = await self.bot.pool_acquire()
        try:
            sql = "DELETE FROM gmc_token_box_req_token WHERE id_gmc_token_box_req = $1"
            await conn.execute(sql, gmcBoxReq.id)
        finally: 
            await self.bot.pool_release(conn)
