def show_analysis(analysis):
    if not isinstance(analysis, list):
        print("⚠️ show_analysis bir liste bekler, dict verdin. 'moves' listesini geçir.")
        return
    for i, move_data in enumerate(analysis, start=1):
        et = move_data["eval"]["type"]
        ev = move_data["eval"]["value"]
        print(f"{i}. {move_data['san']} — [{et}:{ev}] → {move_data['comment']}")
