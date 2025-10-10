def show_analysis(analysis):
    print("📊 Oyun Analizi:\n")
    for i, move_data in enumerate(analysis, start=1):
        eval_type = move_data["eval"]["type"]
        val = move_data["eval"]["value"]
        print(f"{i}. {move_data['move']} — [{eval_type}:{val}] → {move_data['comment']}")
