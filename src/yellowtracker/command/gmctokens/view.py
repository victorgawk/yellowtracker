import discord

from .domain import *

__all__ = (
    'GmcTokensView',
)

class GmcTokensView(discord.ui.View):
    def __init__(self, *, timeout = None, gmcTokenUser: GmcTokenUser):
        super().__init__(timeout = timeout)
        if len(gmcTokenUser.accs) > 0:
            self.add_item(GmcAccountSelect(gmcTokenUser = gmcTokenUser))
        self.add_item(AddAccountButton(gmcTokenUser = gmcTokenUser))

class GmcAccountSelect(discord.ui.Select):
    def __init__(self, gmcTokenUser: GmcTokenUser):
        self.gmcTokenUser = gmcTokenUser
        options = []
        for i in range(len(gmcTokenUser.accs)):
            options.append(discord.SelectOption(label = f"Acc {i + 1}", value = f"{i}"))
        super().__init__(placeholder = "Select an account", options = options)
    async def callback(self, interaction: discord.Interaction):
        accIdSelected = int(self.values[0])
        await interaction.response.edit_message(embed = self.gmcTokenUser.embed(), view = EditAccountView(gmcTokenUser = self.gmcTokenUser, accId = accIdSelected))

class AddAccountButton(discord.ui.Button):
    def __init__(self, gmcTokenUser: GmcTokenUser):
        self.gmcTokenUser = gmcTokenUser
        super().__init__(style = discord.ButtonStyle.primary, emoji = "➕", label = "Add Account", disabled = len(gmcTokenUser.accs) > 2)
    async def callback(self, interaction: discord.Interaction):
        await self.gmcTokenUser.add_account()
        await interaction.response.edit_message(embed = self.gmcTokenUser.embed(), view = GmcTokensView(gmcTokenUser = self.gmcTokenUser))

class EditAccountView(discord.ui.View):
    def __init__(self, *, timeout = None, gmcTokenUser: GmcTokenUser, accId: int, gmcToken: GmcToken = None):
        super().__init__(timeout = timeout)
        self.add_item(GmcTokenSelect(gmcTokenUser = gmcTokenUser, accId = accId, gmcToken = gmcToken))
        self.add_item(GoToGmcTokensViewButton(gmcTokenUser = gmcTokenUser))
        self.add_item(EditBoxRequirementsButton(gmcTokenUser = gmcTokenUser, accId = accId))
        self.add_item(RemoveAccountButton(gmcTokenUser = gmcTokenUser, accId = accId))

class GmcTokenSelect(discord.ui.Select):
    def __init__(self, gmcTokenUser: GmcTokenUser, accId: int, gmcToken: GmcToken = None):
        self.gmcTokenUser = gmcTokenUser
        self.accId = accId
        self.gmcToken = gmcToken
        options = []
        for gmcToken in GmcToken:
            options.append(discord.SelectOption(label = gmcToken.value, value = gmcToken.value, default = (gmcToken == self.gmcToken)))
        super().__init__(placeholder = "Select a Token To Edit", options = options, min_values = 0)
    async def callback(self, interaction: discord.Interaction):
        gmcTokenSelected = None
        if len(self.values) > 0:
            for gmcToken in GmcToken:
                if gmcToken.value == self.values[0]:
                    gmcTokenSelected = gmcToken
                    break
            await interaction.response.send_modal(EditTokenAmountModal(gmcTokenUser = self.gmcTokenUser, accId = self.accId, gmcToken = gmcTokenSelected))
        else:
            await interaction.response.edit_message(embed = self.gmcTokenUser.embed(), view = EditAccountView(gmcTokenUser = self.gmcTokenUser, accId = self.accId, gmcToken = gmcTokenSelected))

class GoToGmcTokensViewButton(discord.ui.Button):
    def __init__(self, gmcTokenUser: GmcTokenUser):
        self.gmcTokenUser = gmcTokenUser
        super().__init__(style = discord.ButtonStyle.primary, emoji = "⬅️", label = "Go Back")
    async def callback(self, interaction: discord.Interaction):
        await interaction.response.edit_message(embed = self.gmcTokenUser.embed(), view = GmcTokensView(gmcTokenUser = self.gmcTokenUser))

class EditTokenAmountModal(discord.ui.Modal):
    def __init__(self, gmcTokenUser: GmcTokenUser, accId: int, gmcToken: GmcToken):
        super().__init__(title = f"Edit {gmcToken.value} Amount for Acc {accId + 1}")
        self.gmcTokenUser = gmcTokenUser
        self.accId = accId
        self.gmcToken = gmcToken
        self.amount_input = discord.ui.TextInput(label = "Amount", default = f"{self.gmcTokenUser.get_token_amount(self.accId, self.gmcToken)}", min_length = 1, max_length = 2)
        self.add_item(self.amount_input)
    async def on_submit(self, interaction: discord.Interaction):
        if self.amount_input.value.isnumeric():
            intval = int(self.amount_input.value)
            if intval >= 0:
                await self.gmcTokenUser.set_token_amount(self.accId, self.gmcToken, intval)
        await interaction.response.edit_message(embed = self.gmcTokenUser.embed(), view = EditAccountView(gmcTokenUser = self.gmcTokenUser, accId = self.accId, gmcToken = self.gmcToken))

class EditBoxRequirementsButton(discord.ui.Button):
    def __init__(self, gmcTokenUser: GmcTokenUser, accId: int):
        self.gmcTokenUser = gmcTokenUser
        self.accId = accId
        super().__init__(style = discord.ButtonStyle.primary, emoji = "🎁", label = "Edit Box Requirements")
    async def callback(self, interaction: discord.Interaction):
        await interaction.response.edit_message(view = EditBoxRequirementsView(gmcTokenUser = self.gmcTokenUser, accId = self.accId))

class EditBoxRequirementsView(discord.ui.View):
    def __init__(self, *, timeout = None, gmcTokenUser: GmcTokenUser, accId: int, gmcBox: GmcBox = None, gmcTokens: list[GmcToken] = []):
        super().__init__(timeout = timeout)
        self.add_item(GmcBoxSelect(gmcTokenUser = gmcTokenUser, accId = accId, gmcBox = gmcBox, gmcTokens = gmcTokens))
        self.add_item(BoxRequirementsSelect(gmcTokenUser = gmcTokenUser, accId = accId, gmcBox = gmcBox, gmcTokens = gmcTokens))
        self.add_item(GoToEditAccountViewButton(gmcTokenUser = gmcTokenUser, accId = accId))
        self.add_item(ClaimGmcBoxButton(gmcTokenUser = gmcTokenUser, accId = accId, gmcBox = gmcBox, gmcTokens = gmcTokens))
        self.add_item(ClaimGmcNormalBoxButton(gmcTokenUser = gmcTokenUser, accId = accId, gmcBox = gmcBox, gmcTokens = gmcTokens))

class GmcBoxSelect(discord.ui.Select):
    def __init__(self, gmcTokenUser: GmcTokenUser, accId: int, gmcBox: GmcBox, gmcTokens: list[GmcToken]):
        self.gmcTokenUser = gmcTokenUser
        self.accId = accId
        self.gmcBox = gmcBox
        self.gmcTokens = gmcTokens
        options = []
        for gmcBox in GmcBox:
            options.append(discord.SelectOption(label = gmcBox.value, value = gmcBox.value, default = (gmcBox == self.gmcBox)))
        super().__init__(placeholder = "Select a box", options = options)
    async def callback(self, interaction: discord.Interaction):
        gmcBoxSelected = None
        for gmcBox in GmcBox:
            if gmcBox.value == self.values[0]:
                gmcBoxSelected = gmcBox
                break
        gmcTokensSelected = self.gmcTokenUser.get_tokens_req(self.accId, gmcBoxSelected)
        await interaction.response.edit_message(view = EditBoxRequirementsView(gmcTokenUser = self.gmcTokenUser, accId = self.accId, gmcBox = gmcBoxSelected, gmcTokens = gmcTokensSelected))

class BoxRequirementsSelect(discord.ui.Select):
    def __init__(self, gmcTokenUser: GmcTokenUser, accId: int, gmcBox: GmcBox, gmcTokens: list[GmcToken]):
        self.gmcTokenUser = gmcTokenUser
        self.accId = accId
        self.gmcBox = gmcBox
        self.gmcTokens = gmcTokens
        options = []
        for gmcToken in GmcToken:
            options.append(discord.SelectOption(label = gmcToken.value, value = gmcToken.value, default = (gmcToken in gmcTokens)))
        super().__init__(placeholder = "Select box requirements", options = options, min_values = 5, max_values = 5, disabled = (gmcBox is None))
    async def callback(self, interaction: discord.Interaction):
        gmcTokensSelected = []
        for gmcToken in GmcToken:
            if gmcToken.value in self.values:
                gmcTokensSelected.append(gmcToken)
        await self.gmcTokenUser.set_box_requirements(self.accId, self.gmcBox, gmcTokensSelected)
        await interaction.response.edit_message(embed = self.gmcTokenUser.embed(), view = EditBoxRequirementsView(gmcTokenUser = self.gmcTokenUser, accId = self.accId, gmcBox = self.gmcBox, gmcTokens = gmcTokensSelected))

class GoToEditAccountViewButton(discord.ui.Button):
    def __init__(self, gmcTokenUser: GmcTokenUser, accId: int):
        self.gmcTokenUser = gmcTokenUser
        self.accId = accId
        super().__init__(style = discord.ButtonStyle.primary, emoji = "⬅️", label = "Go Back")
    async def callback(self, interaction: discord.Interaction):
        await interaction.response.edit_message(embed = self.gmcTokenUser.embed(), view = EditAccountView(gmcTokenUser = self.gmcTokenUser, accId = self.accId))

class ClaimGmcBoxButton(discord.ui.Button):
    def __init__(self, gmcTokenUser: GmcTokenUser, accId: int, gmcBox: GmcBox, gmcTokens: list[GmcToken]):
        self.gmcTokenUser = gmcTokenUser
        self.accId = accId
        self.gmcBox = gmcBox
        self.gmcTokens = gmcTokens
        disabled = (gmcBox is None or len(gmcTokens) == 0 or gmcBox.value not in self.gmcTokenUser.get_claimable_box_names(accId))
        label = f"Claim {'' if gmcBox is None else gmcBox.value} Box"
        super().__init__(style = discord.ButtonStyle.primary, emoji = "🎁", label = label, disabled = disabled)
    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_modal(ClaimGmcBoxModal(gmcTokenUser = self.gmcTokenUser, accId = self.accId, gmcBox = self.gmcBox, gmcTokens = self.gmcTokens))

class ClaimGmcBoxModal(discord.ui.Modal):
    def __init__(self, gmcTokenUser: GmcTokenUser, accId: int, gmcBox: GmcBox, gmcTokens: list[GmcToken]):
        super().__init__(title = f"Claim {gmcBox.value} Box on Acc {accId + 1}")
        self.gmcTokenUser = gmcTokenUser
        self.accId = accId
        self.gmcBox = gmcBox
        self.gmcTokens = gmcTokens
        self.yes_input = discord.ui.TextInput(label = "Type yes to confirm", placeholder="yes", min_length = 1, max_length = 3)
        self.add_item(self.yes_input)
    async def on_submit(self, interaction: discord.Interaction):
        if self.yes_input.value == "yes":
            await self.gmcTokenUser.claim_box(self.accId, self.gmcBox)
            self.gmcTokens = []
        await interaction.response.edit_message(embed = self.gmcTokenUser.embed(), view = EditBoxRequirementsView(gmcTokenUser = self.gmcTokenUser, accId = self.accId, gmcBox = self.gmcBox, gmcTokens = self.gmcTokens))

class ClaimGmcNormalBoxButton(discord.ui.Button):
    def __init__(self, gmcTokenUser: GmcTokenUser, accId: int, gmcBox: GmcBox, gmcTokens: list[GmcToken]):
        self.gmcTokenUser = gmcTokenUser
        self.accId = accId
        self.gmcBox = gmcBox
        self.gmcTokens = gmcTokens
        super().__init__(style = discord.ButtonStyle.primary, emoji = "🎁", label = "Claim Normal Box", disabled = not self.gmcTokenUser.is_normal_box_claimable(accId))
    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_modal(ClaimGmcNormalBoxModal(gmcTokenUser = self.gmcTokenUser, accId = self.accId, gmcBox = self.gmcBox, gmcTokens = self.gmcTokens))

class ClaimGmcNormalBoxModal(discord.ui.Modal):
    def __init__(self, gmcTokenUser: GmcTokenUser, accId: int, gmcBox: GmcBox, gmcTokens: list[GmcToken]):
        super().__init__(title = f"Claim Normal Box on Acc {accId + 1}")
        self.gmcTokenUser = gmcTokenUser
        self.accId = accId
        self.gmcBox = gmcBox
        self.gmcTokens = gmcTokens
        self.yes_input = discord.ui.TextInput(label = "Type yes to confirm", placeholder="yes", min_length = 1, max_length = 3)
        self.add_item(self.yes_input)
    async def on_submit(self, interaction: discord.Interaction):
        if self.yes_input.value == "yes":
            await self.gmcTokenUser.claim_normal_box(self.accId)
            self.gmcTokens = []
        await interaction.response.edit_message(embed = self.gmcTokenUser.embed(), view = EditBoxRequirementsView(gmcTokenUser = self.gmcTokenUser, accId = self.accId, gmcBox = self.gmcBox, gmcTokens = self.gmcTokens))

class RemoveAccountButton(discord.ui.Button):
    def __init__(self, gmcTokenUser: GmcTokenUser, accId: int):
        self.gmcTokenUser = gmcTokenUser
        self.accId = accId
        super().__init__(style = discord.ButtonStyle.primary, emoji = "🗑️", label = f"Delete Acc {accId + 1}")
    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_modal(RemoveAccountModal(gmcTokenUser = self.gmcTokenUser, accId = self.accId))

class RemoveAccountModal(discord.ui.Modal):
    def __init__(self, gmcTokenUser: GmcTokenUser, accId: int):
        super().__init__(title = f"Delete Acc {accId + 1}")
        self.gmcTokenUser = gmcTokenUser
        self.accId = accId
        self.yes_input = discord.ui.TextInput(label = "Type yes to confirm", placeholder="yes", min_length = 1, max_length = 3)
        self.add_item(self.yes_input)
    async def on_submit(self, interaction: discord.Interaction):
        if self.yes_input.value == "yes":
            await self.gmcTokenUser.delete_account(self.accId)
            await interaction.response.edit_message(embed = self.gmcTokenUser.embed(), view = GmcTokensView(gmcTokenUser = self.gmcTokenUser))
        else:
            await interaction.response.edit_message(embed = self.gmcTokenUser.embed(), view = EditAccountView(gmcTokenUser = self.gmcTokenUser, accId = self.accId))
