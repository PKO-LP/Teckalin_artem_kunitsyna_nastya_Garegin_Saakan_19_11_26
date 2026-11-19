import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import simpledialog

games = []  # данные: список словарей


def refresh_list(rows=None):
    """Перерисовывает таблицу (по умолчанию — все игры)."""
    tree.delete(*tree.get_children())
    for g in (rows if rows is not None else games):
        tree.insert("", tk.END, values=(g["name"], g["genre"], g["players"], g["status"]))


def selected_game():
    sel = tree.selection()
    if not sel:
        messagebox.showinfo("Внимание", "Выберите игру в списке")
        return None
    name = tree.item(sel[0])["values"][0]
    for g in games:
        if g["name"] == name:
            return g
    return None


def add_game():
    name, genre, players = name_entry.get().strip(), genre_entry.get().strip(), players_entry.get().strip()

    if not name or not genre:
        messagebox.showwarning("Проверка", "Название и жанр — обязательные поля")
        return
    if not players.replace("-", "").isdigit():
        messagebox.showwarning("Проверка", "Укажите игроков в формате 2-4")
        return

    games.append({"name": name, "genre": genre, "players": players, "status": "в клубе"})
    name_entry.delete(0, tk.END)
    genre_entry.delete(0, tk.END)
    players_entry.delete(0, tk.END)
    refresh_list()


def book_game():
    game = selected_game()
    if game is None:
        return
    if game["status"] == "выдана":
        messagebox.showwarning("Бронирование", "Игра уже выдана")
        return
    player = simpledialog.askstring("Бронирование", "Имя игрока:", parent=root)
    if player:  # пустая строка или «Отмена» — ничего не делаем
        game["status"] = "выдана"
        refresh_list()


def return_game():
    game = selected_game()
    if game and game["status"] == "выдана":
        game["status"] = "в клубе"
        refresh_list()


def delete_game():
    game = selected_game()
    if game and messagebox.askyesno("Удаление", f"Удалить игру «{game['name']}»?"):
        games.remove(game)
        refresh_list()


def search_games(_event=None):
    query = search_entry.get().strip().lower()
    refresh_list([g for g in games
                  if query in g["name"].lower() or query in g["genre"].lower()])

# ---------- Интерфейс ----------

root = tk.Tk()
root.title("MyGamesHub")
root.geometry("700x450")

form = ttk.Frame(root)
form.pack(pady=5)

name_entry = ttk.Entry(form, width=25)
genre_entry = ttk.Entry(form, width=15)
players_entry = ttk.Entry(form, width=8)
for i, (label, widget) in enumerate([("Название", name_entry), ("Жанр", genre_entry), ("Игроков", players_entry)]):
    ttk.Label(form, text=label).grid(row=0, column=i * 2, padx=3)
    widget.grid(row=0, column=i * 2 + 1, padx=3)

ttk.Button(form, text="Добавить", command=add_game).grid(row=1, column=0, columnspan=6, pady=5)

search_entry = ttk.Entry(root, width=40)
search_entry.pack(pady=5)
search_entry.bind("<KeyRelease>", search_games)

columns = ("name", "genre", "players", "status")
tree = ttk.Treeview(root, columns=columns, show="headings")
for col, title, width in [("name", "Название", 250), ("genre", "Жанр", 120),
                          ("players", "Игроков", 80), ("status", "Статус", 100)]:
    tree.heading(col, text=title)
    tree.column(col, width=width)
tree.pack(fill=tk.BOTH, expand=True)

buttons = ttk.Frame(root)
buttons.pack(pady=5)
ttk.Button(buttons, text="Забронировать", command=book_game).pack(side=tk.LEFT, padx=3)
ttk.Button(buttons, text="Вернуть", command=return_game).pack(side=tk.LEFT, padx=3)
ttk.Button(buttons, text="Удалить", command=delete_game).pack(side=tk.LEFT, padx=3)

root.mainloop()