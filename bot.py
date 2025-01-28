import discord
from discord import app_commands
import mysql.connector
from datetime import datetime
import pytz
from discord.ui import Select, View

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'gruener_faktencheck'
}

def setup_database():
    conn = mysql.connector.connect(**db_config)
    
    conn.execute("""
        CREATE TABLE IF NOT EXISTS categories (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL
        )
    """)
    
    conn.execute("""
        CREATE TABLE IF NOT EXISTS articles (
            id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            url TEXT NOT NULL,
            description TEXT,
            category_id INT,
            published_date DATE,
            FOREIGN KEY (category_id) REFERENCES categories(id)
        ) ENGINE=InnoDB
    """)
    
    try:
        conn.execute("""
            ALTER TABLE articles 
            ADD COLUMN description TEXT 
            AFTER url
        """)
        conn.commit()
        print("Added description column to articles table")
    except mysql.connector.Error as err:
        if err.errno == 1060:
            pass
        else:
            print(f"Error adding description column: {err}")
    
    conn.close()

setup_database()

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

def get_db_connection():
    return mysql.connector.connect(**db_config)

# Modal für die Kategorieeingabe
class CategoryModal(discord.ui.Modal, title='Kategorie hinzufügen'):
    name = discord.ui.TextInput(
        label='📝 Kategorie Name',
        placeholder='Gib den Namen der neuen Kategorie ein...',
        required=True,
        min_length=2,
        max_length=100
    )

    async def on_submit(self, interaction: discord.Interaction):
        try:
            conn = get_db_connection()
            conn.execute("INSERT INTO categories (name) VALUES (%s)", (str(self.name),))
            conn.commit()
            
            success_embed = discord.Embed(
                title="Neue Kategorie erstellt",
                description=f"Die Kategorie wurde erfolgreich angelegt!",
                color=discord.Color.brand_green()
            )
            success_embed.add_field(
                name="📝 Kategorie Name",
                value=f"```{self.name}```",
                inline=False
            )
            success_embed.set_footer(text="Made with ♡ by Finduss • /list_categories um alle Kategorien anzuzeigen")
            
            await interaction.response.send_message(embed=success_embed, ephemeral=True)
        except Exception as e:
            error_embed = discord.Embed(
                title="❌ Fehler aufgetreten",
                description="Bei der Erstellung der Kategorie ist ein Fehler aufgetreten.",
                color=discord.Color.brand_red()
            )
            error_embed.add_field(
                name="🔍 Fehlermeldung",
                value=f"```{str(e)}```",
                inline=False
            )
            error_embed.set_footer(text="Made with ♡ by Finduss")
            await interaction.response.send_message(embed=error_embed, ephemeral=True)
        finally:
            conn.close()

# Update the command handlers to use the modals
@tree.command(name="add_category", description="Füge eine neue Kategorie hinzu")
async def add_category(interaction: discord.Interaction):
    modal = CategoryModal()
    await interaction.response.send_modal(modal)

@tree.command(name="list_categories", description="Zeige alle verfügbaren Kategorien an")
async def list_categories(interaction: discord.Interaction):
    try:
        conn = get_db_connection()
        result = conn.execute("SELECT id, name FROM categories ORDER BY name")
        categories = result.fetchall()
        
        if not categories:
            embed = discord.Embed(
                title="📋 Kategorieübersicht",
                description="```Es wurden noch keine Kategorien angelegt.```",
                color=discord.Color.brand_red()
            )
            embed.add_field(
                name="💡 Tipp",
                value="Nutze `/add_category` um eine neue Kategorie anzulegen!",
                inline=False
            )
            embed.set_footer(text="Made with ♡ by Finduss")
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
            
        embed = discord.Embed(
            title="📋 Kategorieübersicht",
            description="Hier findest du alle verfügbaren Kategorien:",
            color=discord.Color.brand_green()
        )
        
        # Group categories in chunks of 3 for better formatting
        for i in range(0, len(categories), 3):
            chunk = categories[i:i+3]
            for cat_id, name in chunk:
                embed.add_field(
                    name=f"🏷️ ID: {cat_id}",
                    value=f"```{name}```",
                    inline=True
                )
        
        total_categories = len(categories)
        embed.add_field(
            name="📊 Statistik",
            value=f"Insgesamt {total_categories} Kategorie{'n' if total_categories != 1 else ''}",
            inline=False
        )
        embed.set_footer(text="Made with ♡ by Finduss • /add_category um eine neue Kategorie hinzuzufügen")
        
        await interaction.response.send_message(embed=embed, ephemeral=True)
        
    except Exception as e:
        error_embed = discord.Embed(
            title="❌ Fehler aufgetreten",
            description="Beim Abrufen der Kategorien ist ein Fehler aufgetreten.",
            color=discord.Color.brand_red()
        )
        error_embed.add_field(
            name="🔍 Fehlermeldung",
            value=f"```{str(e)}```",
            inline=False
        )
        error_embed.set_footer(text="Made with ♡ by Finduss")
        await interaction.response.send_message(embed=error_embed, ephemeral=True)
    finally:
        conn.close()

# Modal für die Artikeleingabe
class ArticleModal(discord.ui.Modal, title='📝 Artikel hinzufügen'):
    title = discord.ui.TextInput(
        label='📌 Artikel Titel',
        placeholder='Gib den Titel des Artikels ein...',
        required=True,
        min_length=3,
        max_length=255
    )
    
    url = discord.ui.TextInput(
        label='🔗 Artikel URL',
        placeholder='https://...',
        required=True,
        min_length=5,
        max_length=500
    )
    
    description = discord.ui.TextInput(
        label='📄 Beschreibung',
        placeholder='Gib eine kurze Beschreibung ein. Diese wird auf der Seite angezeigt.',
        style=discord.TextStyle.paragraph,
        required=True,
        min_length=10,
        max_length=1000
    )
    
    published_date = discord.ui.TextInput(
        label='📅 Veröffentlichungsdatum',
        placeholder='Format: TT.MM.JJJJ (z.B. 25.01.2024)',
        required=True,
        min_length=10,
        max_length=10
    )

    async def on_submit(self, interaction: discord.Interaction):
        try:
            date_obj = datetime.strptime(str(self.published_date), "%d.%m.%Y")
            formatted_date = date_obj.strftime("%Y-%m-%d")
        except ValueError:
            error_embed = discord.Embed(
                title="❌ Ungültiges Datum",
                description="Das eingegebene Datum entspricht nicht dem korrekten Format.",
                color=discord.Color.brand_red()
            )
            error_embed.add_field(
                name="💡 Korrektes Format",
                value="```TT.MM.JJJJ (z.B. 25.01.2024)```",
                inline=False
            )
            error_embed.set_footer(text="Made with ♡ by Finduss")
            await interaction.response.send_message(embed=error_embed, ephemeral=True)
            return

        view = CategoryView(self.categories)
        category_embed = discord.Embed(
            title="🗂️ Kategorie auswählen",
            description="Bitte wähle eine passende Kategorie für deinen Artikel:",
            color=discord.Color.blurple()
        )
        category_embed.set_footer(text="Made with ♡ by Finduss")
        await interaction.response.send_message(embed=category_embed, view=view, ephemeral=True)
        
        await view.wait()
        
        if view.selected_category:
            category_id = int(view.selected_category)
            conn = get_db_connection()
            
            try:
                conn.execute(
                    "INSERT INTO articles (title, url, description, category_id, published_date) VALUES (%s, %s, %s, %s, %s)",
                    (str(self.title), str(self.url), str(self.description), category_id, formatted_date)
                )
                conn.commit()
                
                success_embed = discord.Embed(
                    title="Artikel erfolgreich erstellt",
                    description="Dein Artikel wurde erfolgreich in der Datenbank gespeichert!",
                    color=discord.Color.brand_green()
                )
                success_embed.add_field(
                    name="📌 Titel",
                    value=f"```{self.title}```",
                    inline=False
                )
                success_embed.add_field(
                    name="📅 Veröffentlicht am",
                    value=f"```{self.published_date}```",
                    inline=True
                )
                success_embed.add_field(
                    name="🔗 URL",
                    value=f"```{self.url}```",
                    inline=False
                )
                success_embed.add_field(
                    name="📄 Beschreibung",
                    value=f"```{self.description}```",
                    inline=False
                )
                success_embed.set_footer(text="Made with ♡ by Finduss")
                
                await interaction.followup.send(embed=success_embed, ephemeral=True)
            except Exception as e:
                error_embed = discord.Embed(
                    title="❌ Fehler aufgetreten",
                    description="Beim Speichern des Artikels ist ein Fehler aufgetreten.",
                    color=discord.Color.brand_red()
                )
                error_embed.add_field(
                    name="🔍 Fehlermeldung",
                    value=f"```{str(e)}```",
                    inline=False
                )
                error_embed.set_footer(text="Made with ♡ by Finduss")
                await interaction.followup.send(embed=error_embed, ephemeral=True)
            finally:
                conn.close()
        else:
            error_embed = discord.Embed(
                title="❌ Keine Kategorie ausgewählt",
                description="Der Vorgang wurde abgebrochen, da keine Kategorie ausgewählt wurde.",
                color=discord.Color.brand_red()
            )
            error_embed.add_field(
                name="💡 Tipp",
                value="Versuche es erneut und wähle eine Kategorie aus der Liste aus.",
                inline=False
            )
            error_embed.set_footer(text="Made with ♡ by Finduss")
            await interaction.followup.send(embed=error_embed, ephemeral=True)

# Fügt einen neuen Artikel hinzu
@tree.command(name="add_article", description="Füge einen neuen Artikel hinzu")
async def add_article(interaction: discord.Interaction):
    conn = get_db_connection()
    result = conn.execute("SELECT id, name FROM categories")
    categories = result.fetchall()
    conn.close()
    
    if not categories:
        await interaction.response.send_message(
            "Keine Kategorien gefunden. Bitte erstelle zuerst eine Kategorie.", 
            ephemeral=True
        )
        return

    modal = ArticleModal(categories)
    await interaction.response.send_modal(modal)

@client.event
async def on_ready():
    await tree.sync()
    print(f'Bot is ready! Logged in as {client.user}')

class CategorySelect(Select):
    def __init__(self, categories):
        options = [
            discord.SelectOption(
                label=category[1],
                value=str(category[0]),
                description=f"Wähle {category[1]}"
            ) for category in categories
        ]
        super().__init__(
            placeholder="Wähle eine Kategorie...", 
            min_values=1, 
            max_values=1, 
            options=options
        )

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()
        self.view.selected_category = self.values[0]
        self.view.stop()

class CategoryView(View):
    def __init__(self, categories):
        super().__init__(timeout=180)
        self.selected_category = None
        self.add_item(CategorySelect(categories))

client.run('bot token')
