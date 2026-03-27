from flask import Flask, render_template, request, redirect

app = Flask(__name__)

players = [
    {"name": f"Player{i}", "score": (i * 37) % 501, "wins": (i * 3) % 20, "losses": (i * 5) % 15}
    for i in range(1, 101)
]

def games_played(player):
    return player["wins"] + player["losses"]

def merge_sort(players, key):
    if len(players) <= 1:
        return players

    mid = len(players) // 2
    left = merge_sort(players[:mid], key)
    right = merge_sort(players[mid:], key)

    return merge(left, right, key)

def merge(left, right, key):
    result = []
    i = j = 0

    while i < len(left) and j < len(right):
        if key(left[i]) > key(right[j]):  # dynamic comparison
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    result.extend(left[i:])
    result.extend(right[j:])
    return result

def key_value(player, sort_by):
    if sort_by == "wins":
        return player["wins"]
    elif sort_by == "losses":
        return player["losses"]
    elif sort_by == "games":
        return player["wins"] + player["losses"]
    return player["score"]


@app.route("/", methods=["GET", "POST"])
def index():
    global players

    search_name = request.args.get("search", "").strip()
    sort_by = request.args.get("sort", "score")  # default sort

    # Define sorting logic
    if sort_by == "wins":
        sorted_players = merge_sort(players, key=lambda p: p["wins"])
    elif sort_by == "losses":
        sorted_players = merge_sort(players, key=lambda p: p["losses"])
    elif sort_by == "games":
        sorted_players = merge_sort(players, key=lambda p: p["wins"] + p["losses"])
    else:
        sorted_players = merge_sort(players, key=lambda p: p["score"])

    message = ""

    if search_name:
        found = False
        for i, player in enumerate(sorted_players):
            if player["name"].lower() == search_name.lower():
                message = f"Player {player['name']} is found at rank {i+1} with {sort_by} = {key_value(player, sort_by)}"
                found = True
                break
        
        if not found:
            message = f"Player {search_name} is not found or the name is wrong"

    return render_template(
        "index.html",
        players=sorted_players,
        search=search_name,
        message=message,
        sort=sort_by
    )

@app.route("/add", methods=["POST"])
def add():
    players.append({
        "name": request.form["name"],
        "score": int(request.form["score"]),
        "wins": int(request.form["wins"]),
        "losses": int(request.form["losses"])
    })
    return redirect("/")


@app.route("/delete/<name>")
def delete(name):
    global players
    players = [p for p in players if p["name"] != name]
    return redirect("/")

def to_int(value, default):
    try:
        return int(value)
    except (TypeError, ValueError):
        return default

@app.route("/edit", methods=["POST"])
def edit():
    for p in players:
        if p["name"] == request.form["old_name"]:
            
            if request.form.get("new_name"):
                p["name"] = request.form["new_name"]
            
            if request.form.get("score"):
                p["score"] = int(request.form["score"])
            
            if request.form.get("wins"):
                p["wins"] = int(request.form["wins"])
            
            if request.form.get("losses"):
                p["losses"] = int(request.form["losses"])
            
            break

    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)