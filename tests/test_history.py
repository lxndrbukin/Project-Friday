import utils

def test_save_new_history(tmp_path, monkeypatch):
    monkeypatch.setattr(utils, "HISTORY_DIR", str(tmp_path))
    result = utils.save_history(
        conv_id=None,
        title="test_title",
        previous_interaction_id=None,
        messages=[]
    )
    assert (tmp_path / f"{result}.json").exists()

def test_save_existing_history(tmp_path, monkeypatch):
    monkeypatch.setattr(utils, "HISTORY_DIR", str(tmp_path))
    new_conv_id = utils.save_history(
        conv_id=None,
        title="test_title",
        previous_interaction_id=None,
        messages=[]
    )
    utils.save_history(
        conv_id=new_conv_id,
        messages=[
            {"role": "user", "content": "test_prompt"},
            {"role": "assistant", "content": "test_answer"},
        ]
    )
    data = utils.fetch_history(new_conv_id)
    assert data["messages"] == [
        {"role": "user", "content": "test_prompt"},
        {"role": "assistant", "content": "test_answer"},
    ]