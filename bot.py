import discord
import ast
import io
import os
import re
from discord.ext import commands
from discord import Embed
from discord import Color


intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=".", intents=intents)
option_id = 0


class Dropdown(discord.ui.Select):
    def __init__(self, folder_path):
        global option_id
        option_id = 0  # Reiniciar el contador para cada nuevo menú desplegable
        folder_name = os.path.basename(folder_path)
        options, self.data = self.get_options(folder_path)
        super().__init__(placeholder=folder_name, options=options)

    def get_options(self, folder_path):
        global option_id
        options = []
        data = {}
        for item_name in os.listdir(folder_path):
            item_path = os.path.join(folder_path, item_name)
            if os.path.isdir(item_path):
                sub_options, sub_data = self.get_options(item_path)
                options.extend(sub_options)
                data.update(sub_data)
            else:
                label_name, ext = os.path.splitext(item_name)
                if ext == ".txt":
                    label_folder = os.path.basename(folder_path)
                    value = str(option_id)
                    options.append(discord.SelectOption(label=label_name, value=value))

                    txt_file_path = os.path.join(folder_path, f"{label_name}.txt")
                    image_file_path = os.path.join(folder_path, f"{label_name}.png")

                    with open(txt_file_path, "r") as txt_file:
                        text = txt_file.read()

                    with open(image_file_path, "rb") as image_file:
                        image = image_file.read()

                    data[value] = (text, image)
                    option_id += 1  # Incrementar el contador de IDs de las opciones
        return options, data

    async def callback(self, interaction: discord.Interaction):

        value = self.values[0]
        text, image = self.data[value]
        selected_option = next(
            option for option in self.options if option.value == value
        )

        # Almacena el nombre del label en una variable
        selected_label = selected_option.label

        embed = discord.Embed(
            title=f"you have selected: {selected_label}", color=0x0000FF
        )
        embed.description = text
        embed.set_thumbnail(url=f"attachment://{value}.png")
        embed.set_image(url="https://s13.gifyu.com/images/S0gM8.gif")
        embed.set_footer(
            text="SlashService For All Your 07/RS3 Gold & Runescape Service Needs",
            icon_url="https://s13.gifyu.com/images/S0gxY.gif",
        )

        file = discord.File(io.BytesIO(image), filename=f"{value}.png")
        await interaction.response.send_message(file=file, embed=embed, ephemeral=True)

        # Restablecer el combobox al placeholder
        self.placeholder = os.path.basename(self.placeholder)
        self.value = None
        await interaction.message.edit(view=self.view)


class ServiceButton(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        button = discord.ui.Button(
            label="Buy Services",
            style=discord.ButtonStyle.url,
            url="https://discord.com/channels/1086268937852944484/1086968086646755390",
        )
        self.add_item(button)


class GoldButton(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        button = discord.ui.Button(
            label="Buy/Sell Gold",
            style=discord.ButtonStyle.url,
            url="https://discord.com/channels/1086268937852944484/1086968061757751376",
        )
        self.add_item(button)


@bot.event
async def on_ready():
    print(f"{bot.user} ha iniciado sesión")

@bot.command(name="calc")
async def calc(ctx, *, operation: str):
    # Verifica si la operación es segura para evaluar
    if re.match("^[\d+\-*/.%() ]+$", operation):
        try:
            # Verifica si hay un descuento porcentual
            if '%' in operation:
                # Separa la operación y el descuento
                operation, discount = operation.split('-')
                # Elimina el signo de porcentaje del descuento
                discount = discount.replace('%', '')
                # Evalúa la operación
                total = eval(operation)
                # Calcula el total con descuento
                total_discount = total - (total * float(discount) / 100)
                # Redondea el resultado a 2 decimales
                total_discount_rounded = round(total_discount, 2)
                # Envia el resultado
                await ctx.send(f"{operation}\n\n~~Total = ${total}~~\nTotal With Active Discount = **${total_discount_rounded}**")
            else:
                # Evalúa la operación
                result = eval(operation)
                # Redondea el resultado a 2 decimales
                result_rounded = round(result, 2)
                # Envia el resultado
                await ctx.send(f"{operation}\n\nTotal = **${result_rounded}**")
        except Exception as e:
            # En caso de error, envía a la consola
            print(f"Error al calcular la operación: {str(e)}")
    else:
        await ctx.send("expresión no válida, utiliza solo números y los operadores permitidos: (+, -, *, /, %)")


@bot.command(name="menu1")
async def menu1(ctx):
    roles_autorizados = [
        "Moderator",
        "Owner",
        "Worker Lead",
    ]  # Añade los nombres de los roles autorizados aquí

    try:
        # Verifica si el usuario tiene al menos un rol autorizado
        if any(role.name in roles_autorizados for role in ctx.author.roles):
            view = discord.ui.View(timeout=None)
            root_folder = os.path.dirname(os.path.abspath(__file__))
            dropdowns_folder = os.path.join(root_folder, "Prices", "Menu1")
            for dropdown_folder in os.listdir(dropdowns_folder):
                dropdown_folder_path = os.path.join(dropdowns_folder, dropdown_folder)
                if os.path.isdir(dropdown_folder_path):
                    view.add_item(Dropdown(dropdown_folder_path))
            await ctx.send(view=view)
    except Exception as e:
        print(f"Se produjo un error: {e}")


@bot.command(name="menu2")
async def menu2(ctx):
    roles_autorizados = [
        "Moderator",
        "Owner",
        "Worker Lead",
    ]  # Añade los nombres de los roles autorizados aquí

    try:
        # Verifica si el usuario tiene al menos un rol autorizado
        if any(role.name in roles_autorizados for role in ctx.author.roles):
            view = discord.ui.View(timeout=None)
            root_folder = os.path.dirname(os.path.abspath(__file__))
            dropdowns_folder = os.path.join(root_folder, "Prices", "Menu2")
            for dropdown_folder in os.listdir(dropdowns_folder):
                dropdown_folder_path = os.path.join(dropdowns_folder, dropdown_folder)
                if os.path.isdir(dropdown_folder_path):
                    view.add_item(Dropdown(dropdown_folder_path))
            await ctx.send(view=view)
    except Exception as e:
        print(f"Se produjo un error: {e}")


@bot.command(name="banner")
async def banner(ctx):
    roles_autorizados = [
        "Moderator",
        "Owner",
        "Worker Lead",
    ]  # Añade los nombres de los roles autorizados aquí

    try:
        # Verifica si el usuario tiene al menos un rol autorizado
        if any(role.name in roles_autorizados for role in ctx.author.roles):
            await ctx.send("https://imgur.com/zllOCkZ")
    except Exception as e:
        print(f"Se produjo un error: {e}")


@bot.command(name="sbutton")
async def sbutton(ctx):
    roles_autorizados = [
        "Moderator",
        "Owner",
        "Worker Lead",
    ]  # Añade los nombres de los roles autorizados aquí

    try:
        # Verifica si el usuario tiene al menos un rol autorizado
        if any(role.name in roles_autorizados for role in ctx.author.roles):
            await ctx.send(view=ServiceButton())
    except Exception as e:
        print(f"Se produjo un error: {e}")


@bot.slash_command()
async def dev_status(ctx):  # a slash command will be created with the name "ping"
    if os.path.exists("Development Status.txt"):
        with open("Development Status.txt", "r") as file:
            content = file.read()
        await ctx.respond(content)
    else:
        await ctx.respond("error, file has failed")


@bot.slash_command(
    guild_ids=[1086268937852944484], description="Update GP exchange rates"
)  # Asegúrate de reemplazar esto con el ID de tu servidor
async def gp_rates(
    ctx,
    buy_07: discord.Option(float, "Buy Rate for 07GP"),
    sell_07: discord.Option(float, "Sell Rate for 07GP"),
    buy_rs3: discord.Option(float, "Buy Rate for RS3"),
    sell_rs3: discord.Option(float, "Sell Rate for RS3"),
    channel_id: discord.Option(str, "Channel ID to post rates"),
):
    try:
        await tasas(ctx, buy_07, sell_07, buy_rs3, sell_rs3, channel_id)
        await ctx.respond("Done :))")
    except Exception as e:
        await ctx.respond(f"An unexpected error occurred: {str(e)}")


@bot.command(name="tasas")
async def tasas(ctx, buy_07, sell_07, buy_rs3, sell_rs3, channel_id):
    try:
        # Obtiene el canal por su ID
        target_channel = bot.get_channel(int(channel_id))

        # Verifica si el canal existe
        if target_channel is None:
            raise Exception(
                "I'm sorry but it seems that this channel does not exist or you have entered the wrong ID."
            )

        # Obtiene el historial de mensajes del canal objetivo
        messages = await target_channel.history(limit=1).flatten()

        # Verifica si el historial de mensajes está vacío
        if messages:
            # Verifica si el último mensaje en el canal objetivo fue enviado por el bot
            if messages[0].author == bot.user:
                await messages[
                    0
                ].delete()  # Borra el último mensaje del bot en el canal objetivo

        # Crea un nuevo embed
        embed = Embed(
            title="Current Gold Rates",
            description="**__OSRS Gold__**\n"
            "*We Buy at:* ${}/M\n"
            "*We Sell at:* ${}/M\n"
            "\n"
            "**__RS3 Gold__**\n"
            "*We Buy at:* ${}/M\n"
            "*We Sell at:* ${}/M".format(buy_07, sell_07, buy_rs3, sell_rs3),
            color=Color.blue(),
        )
        embed.set_image(url="https://s13.gifyu.com/images/S0eMJ.gif")
        embed.set_thumbnail(url=f"https://s9.gifyu.com/images/SFtIm.jpg")
        embed.set_footer(
            text="SlashService For All Your 07/RS3 Gold & Runescape Service Needs",
            icon_url="https://s13.gifyu.com/images/S0gxY.gif",
        )

        # Crea la vista con el botón de oro
        view = GoldButton()

        # Envía el embed y la vista al canal objetivo
        await target_channel.send(embed=embed, view=view)

    except discord.Forbidden:
        raise Exception(
            "Sorry, I don't have permissions to delete messages or send messages to that channel."
        )
    except discord.HTTPException:
        raise Exception("There was a problem trying to delete the message or send it.")
    except Exception as e:
        raise Exception(f"error XXX: {str(e)}")


@bot.command(name="dev_status")
async def dev_status(ctx):
    # Comprueba si la ID del autor del mensaje es 551987692015976459
    if str(ctx.message.author.id) == "551987692015976459":
        # Asegúrate de que el archivo 'Development Status.txt' esté en el mismo directorio que tu script de bot
        if os.path.exists("Development Status.txt"):
            with open("Development Status.txt", "r") as file:
                content = file.read()
            await ctx.send(content)


bot.run("token")
