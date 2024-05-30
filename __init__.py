
#http://ankisrs.net/docs/addons.html
#from PyQt6.QtWidgets import QAction 
from aqt.qt import QAction
# import the main window object (mw) 
from aqt import mw
from aqt.utils import showInfo, showText

config = mw.addonManager.getConfig(__name__)

first_kanji = u"\u4e00"
last_kanji = u"\u9faf"
#3040..309F; Hiragana
#30A0..30FF; Katakana
#31F0..31FF; Katakana Phonetic Extensions
#Kanji are between \u4e00-\u9faf

def get_card(collection, card_id ):
    card = collection.get_card(card_id)
    note = card.note()
    return note

def get_word(note):
    kf = config["kanji_field"]
    if kf in note:
        return note[kf]
    else:
        return note[config["kana_field"]]

def i_know_all_kanji_in_word(word:str, known_kanji:str) -> bool :
    wkanji = [k for k in word if (k >= first_kanji) & (k <= last_kanji)]
    kanji_known = [ k in known_kanji for k in wkanji]
    return all(kanji_known)

def unsuspend_learned_words():
    ids_of_learned_kanji = mw.col.find_cards(config["kanj_i_learned_query"])
    known_kanji = "".join(set([mw.col.get_card(card_id).note()["Kanji"] for card_id in ids_of_learned_kanji]))
    
    # Get all the suspended vocab cards 
    target_deck_name = config["target_deck"]
    target_deck = mw.col.decks.by_name(target_deck_name)["id"]
    source_cards_query = config["source_deck_query"]
    ids_of_source_cards = mw.col.find_cards(source_cards_query)

    new_words = [ card_id for card_id in ids_of_source_cards if i_know_all_kanji_in_word(get_word(get_card(mw.col, card_id)), known_kanji)]
    # print(card_id)
    # anki_card = get_card(mw.col, card_id)
    # ankiword = get_word(anki_card)
    # if i_know_all_kanji_in_word(ankiword, known_kanji):
    #     cards = mw.col.getCard(card_id).note().cards()
    mw.col.decks.set_deck(new_words, target_deck) 
    mw.reset()


if config["ShowMenu"]:
    
    add_nid3 = QAction(mw)
    mw.form.menuTools.addAction(add_nid3)
    add_nid3.setText(("Move words with learned Kanji"))
    add_nid3.triggered.connect(unsuspend_learned_words)
