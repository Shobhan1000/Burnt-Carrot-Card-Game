import random
import tkinter as tk
from tkinter import messagebox

# ---------- CARD SETUP ----------
suits = ["Hearts", "Diamonds", "Clubs", "Spades"]
ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]

def card_value(card):
    rank, suit = card
    if rank == "K" and suit in ["Hearts", "Diamonds"]:
        return -1
    if rank in ["J", "Q", "K"]:
        return 10
    if rank == "A":
        return 1
    return int(rank)

startDeck = [(rank, suit) for suit in suits for rank in ranks]

def make_deck(deck):
    random.shuffle(deck)
    return deck

def show_card(card):
    return f"{card[0]} of {card[1]}"

def sum_hand(hand):
    return sum(card_value(c) for c in hand if c)


# ---------- MAIN GAME CLASS ----------
class BurntCarrotGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Burnt Carrot Card Game")

        self.deck = make_deck(startDeck.copy())
        self.player_hand = [self.deck.pop() for _ in range(4)]
        self.computer_hand = [self.deck.pop() for _ in range(4)]
        self.revealed_player = set()
        self.revealed_computer = set(random.sample(range(4), 2))
        self.middle_cards = []
        self.middle_card = None
        self.drawn_card = None
        self.burnt_called = False
        self.viewing_stage = True

        self.build_gui()

    # ---------- GUI SETUP ----------
    def build_gui(self):
        self.info_label = tk.Label(self.root, text="Welcome! Choose 2 cards to view.", font=("Arial", 14))
        self.info_label.pack(pady=10)

        self.hand_frame = tk.Frame(self.root)
        self.hand_frame.pack(pady=10)
        self.card_buttons = []
        for i in range(4):
            btn = tk.Button(self.hand_frame, text=f"Card {i+1}", width=12, height=2, command=lambda i=i: self.view_card(i))
            btn.grid(row=0, column=i, padx=5)
            self.card_buttons.append(btn)

        self.middle_label = tk.Label(self.root, text="Middle: [Hidden]", font=("Arial", 12))
        self.middle_label.pack(pady=10)

        self.control_frame = tk.Frame(self.root)
        self.control_frame.pack(pady=10)

        self.draw_btn = tk.Button(self.control_frame, text="Draw Card", command=self.draw_card, state="disabled")
        self.draw_btn.grid(row=0, column=0, padx=5)

        self.swap_btn = tk.Button(self.control_frame, text="Swap Card", command=self.swap_card, state="disabled")
        self.swap_btn.grid(row=0, column=1, padx=5)

        self.place_btn = tk.Button(self.control_frame, text="Place in Middle", command=self.place_in_middle, state="disabled")
        self.place_btn.grid(row=0, column=2, padx=5)

        self.burnt_btn = tk.Button(self.root, text="Call 'Burnt Carrot'", command=self.call_burnt_carrot, state="disabled")
        self.burnt_btn.pack(pady=10)

        self.menubar = tk.Menu(self.root)
        self.helpMenu = tk.Menu(self.menubar, tearoff=0)
        self.helpMenu.add_command(label="How to Play", command=self.show_instructions)
        self.menubar.add_cascade(label="Help", menu=self.helpMenu)
        self.root.config(menu=self.menubar)

    def show_instructions(self):
        instructions = (
            "Burnt Carrot Card Game Instructions:\n\n"
            "1. You start with 4 hidden cards. Choose 2 to view.\n"
            "2. Draw a card from the deck.\n"
            "3. You can swap the drawn card with one of your cards or place it in the middle.\n"
            "4. If you place a card in the middle, you can try to discard matching rank cards.\n"
            "5. You may also place a card in the middle during the computer's turn if you know you have a matching rank.\n"
            "6. Calling 'Burnt Carrot' ends the game after the computer's turn.\n"
            "7. The player with the lowest total card value wins!"
        )
        messagebox.showinfo("How to Play", instructions)

    # ---------- CORE GAME LOGIC ----------
    def view_card(self, index):
        if not self.viewing_stage:
            return
        if len(self.revealed_player) < 2 and index not in self.revealed_player:
            self.revealed_player.add(index)
            card = self.player_hand[index]
            self.card_buttons[index].config(text=show_card(card), bg="lightgreen")
            self.root.after(2000, lambda i=index: self.card_buttons[i].config(text=f"Card {i+1}", bg="SystemButtonFace"))
            if len(self.revealed_player) == 2:
                self.info_label.config(text="Now draw a card to begin.")
                self.draw_btn.config(state="normal")
                self.viewing_stage = False

    def reshuffle_from_middle(self):
        """Rebuild deck from middle pile when deck runs out."""
        if self.middle_cards:
            cards_to_shuffle = [c for c in self.middle_cards if c != self.middle_card]
            if cards_to_shuffle:
                random.shuffle(cards_to_shuffle)
                self.deck = cards_to_shuffle
                self.middle_cards = [self.middle_card] if self.middle_card else []
                self.info_label.config(text="Deck reshuffled from middle pile!")
            else:
                self.info_label.config(text="No cards available to reshuffle.")

    def draw_card(self):
        if not self.deck:
            self.reshuffle_from_middle()
            if not self.deck:
                self.info_label.config(text="No cards left to draw.")
                return
        self.drawn_card = self.deck.pop()
        self.info_label.config(text=f"You drew {show_card(self.drawn_card)}.")
        self.swap_btn.config(state="normal")
        self.place_btn.config(state="normal")
        self.draw_btn.config(state="disabled")

    def swap_card(self):
        def do_swap(index):
            discarded = self.player_hand[index]
            to_remove = [i for i in self.revealed_player if self.player_hand[i] == discarded]
            for i in to_remove:
                self.revealed_player.discard(i)
            self.player_hand[index] = self.drawn_card
            self.middle_card = discarded
            self.middle_cards.append(discarded)
            self.middle_label.config(text=f"Middle: {show_card(self.middle_card)}")
            self.info_label.config(text=f"Swapped {show_card(discarded)} for {show_card(self.drawn_card)}.")

            if self.drawn_card[0] == "7":
                hidden = [i for i in range(4) if i not in self.revealed_player]
                if hidden:
                    new_view = random.choice(hidden)
                    self.revealed_player.add(new_view)
                    card = self.player_hand[new_view]
                    self.card_buttons[new_view].config(text=show_card(card), bg="lightgreen")
                    self.root.after(2000, lambda i=new_view: self.card_buttons[i].config(text=f"Card {i+1}", bg="SystemButtonFace"))
                    messagebox.showinfo("7 Power!", f"You may peek at one more card: {show_card(card)}")

            self.after_play()
            swap_win.destroy()

        swap_win = tk.Toplevel(self.root)
        swap_win.title("Choose a Card to Swap")
        tk.Label(swap_win, text="Select a card position to swap:").pack(pady=5)
        for i in range(4):
            tk.Button(swap_win, text=f"Card {i+1}", command=lambda i=i: do_swap(i)).pack(pady=2)

    def place_in_middle(self):
        self.middle_card = self.drawn_card
        self.middle_label.config(text=f"Middle: {show_card(self.middle_card)}")
        self.info_label.config(text=f"You placed {show_card(self.drawn_card)} in the middle.")
        self.middle_cards.append(self.middle_card)
        self.after_play()

    # ---------- AFTER PLAY LOGIC ----------
    def after_play(self):
        self.swap_btn.config(state="disabled")
        self.place_btn.config(state="disabled")
        self.burnt_btn.config(state="normal")

        if not self.middle_card:
            return self.root.after(1500, self.computer_turn)

        middle_rank = self.middle_card[0]

        # --- Create popup window ---
        popup = tk.Toplevel(self.root)
        popup.title("Place Matching Card?")
        tk.Label(popup, text=f"Middle card is {show_card(self.middle_card)}", font=("Arial", 12)).pack(pady=10)
        tk.Label(popup, text="If you know a card that matches the middle rank, you can place it down.\nOtherwise click Skip.", font=("Arial", 10)).pack(pady=5)

        button_frame = tk.Frame(popup)
        button_frame.pack(pady=10)

        popup.timer_cancelled = False

        def handle_place(index):
            popup.timer_cancelled = True
            popup.destroy()
            card = self.player_hand[index]
            if card and card[0] == middle_rank and index in self.revealed_player:
                self.info_label.config(text=f"You correctly placed down your {show_card(card)}!")
                self.player_hand[index] = None
                self.card_buttons[index].config(text="Empty", bg="gray")
            else:
                self.info_label.config(text=f"Wrong guess! You must draw a replacement card.")
                if not self.deck:
                    self.reshuffle_from_middle()
                if self.deck:
                    new_card = self.deck.pop()
                    self.player_hand[index] = new_card
                    self.card_buttons[index].config(text=f"Card {index+1}", bg="SystemButtonFace")
                    if index in self.revealed_player:
                        self.revealed_player.remove(index)
            self.root.after(1000, self.computer_turn)

        def skip_turn():
            popup.timer_cancelled = True
            popup.destroy()
            self.info_label.config(text="You skipped your discard chance.")
            self.root.after(1000, self.computer_turn)

        for i, c in enumerate(self.player_hand):
            text = f"Card {i+1}"
            tk.Button(button_frame, text=text, width=18, command=lambda i=i: handle_place(i)).grid(row=0, column=i, padx=5)

        tk.Button(popup, text="Skip", width=10, command=skip_turn).pack(pady=10)

        def timer_expired():
            if not popup.timer_cancelled:
                popup.destroy()
                self.info_label.config(text="Time's up! Moving to computer's turn.")
                self.root.after(1000, self.computer_turn)

        popup.after(10000, timer_expired)

    # ---------- COMPUTER TURN ----------
    def computer_turn(self):
        if not self.deck:
            self.reshuffle_from_middle()
            if not self.deck:
                self.end_game("Deck exhausted!")
                return

        drawn_card = self.deck.pop()
        if random.random() < 0.5:
            idx = random.randint(0, 3)
            discarded = self.computer_hand[idx]
            self.computer_hand[idx] = drawn_card
            if discarded:
                self.middle_card = discarded
                self.middle_cards.append(discarded)
            else:
                # If discarded was None, place drawn card in middle instead
                self.middle_card = drawn_card
                self.middle_cards.append(drawn_card)
        else:
            self.middle_card = drawn_card
            self.middle_cards.append(drawn_card)

        # --- 7 power for computer ---
        if self.middle_card and self.middle_card[0] == "7":
            hidden = [i for i in range(4) if i not in self.revealed_computer and self.computer_hand[i]]
            if hidden:
                new_view = random.choice(hidden)
                self.revealed_computer.add(new_view)

        self.middle_label.config(text=f"Middle: {show_card(self.middle_card)}")
        middle_rank = self.middle_card[0]

        # --- Computer discards if possible ---
        for i, c in enumerate(self.computer_hand):
            if c and c[0] == middle_rank and i in self.revealed_computer:
                self.computer_hand[i] = None

        # --- Player gets chance to play during computer turn ---
        popup = tk.Toplevel(self.root)
        popup.title("Your Chance to Play!")
        tk.Label(popup, text=f"Middle card is {show_card(self.middle_card)}", font=("Arial", 12)).pack(pady=10)
        tk.Label(
            popup,
            text="You can place a card down if you know it matches the middle rank.\nOtherwise click Skip.",
            font=("Arial", 10)
        ).pack(pady=5)

        button_frame = tk.Frame(popup)
        button_frame.pack(pady=10)
        popup.timer_cancelled = False

        def handle_place(index):
            popup.timer_cancelled = True
            popup.destroy()
            card = self.player_hand[index]
            if card and card[0] == middle_rank and index in self.revealed_player:
                self.info_label.config(text=f"You correctly placed down your {show_card(card)}!")
                self.player_hand[index] = None
                self.card_buttons[index].config(text="Empty", bg="gray")
            else:
                self.info_label.config(text=f"Wrong guess! You must draw a replacement card.")
                if not self.deck:
                    self.reshuffle_from_middle()
                if self.deck:
                    new_card = self.deck.pop()
                    self.player_hand[index] = new_card
                    self.card_buttons[index].config(text=f"Card {index+1}", bg="SystemButtonFace")
                    if index in self.revealed_player:
                        self.revealed_player.remove(index)
            self.root.after(1000, self.after_computer_turn)

        def skip_turn():
            popup.timer_cancelled = True
            popup.destroy()
            self.info_label.config(text="You skipped your chance.")
            self.root.after(1000, self.after_computer_turn)

        for i, c in enumerate(self.player_hand):
            text = f"Card {i+1}"
            tk.Button(button_frame, text=text, width=18, command=lambda i=i: handle_place(i)).grid(row=0, column=i, padx=5)

        tk.Button(popup, text="Skip", width=10, command=skip_turn).pack(pady=10)

        def timer_expired():
            if not popup.timer_cancelled:
                popup.destroy()
                self.info_label.config(text="Time's up! Your chance to play is over.")
                self.root.after(1000, self.after_computer_turn)

        popup.after(10000, timer_expired)

    def after_computer_turn(self):
        """Handles transition after computer + player's reaction."""
        if not self.burnt_called:
            self.info_label.config(text="Your turn — draw a new card.")
            self.draw_btn.config(state="normal")
        else:
            self.root.after(1000, lambda: self.end_game("Burnt Carrot called!"))


    # ---------- GAME END ----------
    def call_burnt_carrot(self):
        self.burnt_called = True
        self.info_label.config(text="You called 'Burnt Carrot'! Computer gets one last turn.")
        self.burnt_btn.config(state="disabled")
        self.root.after(2000, self.computer_turn)

    def end_game(self, reason):
        self.info_label.config(text=reason)
        player_total = sum_hand(self.player_hand)
        comp_total = sum_hand(self.computer_hand)
        result = ""
        if player_total < comp_total:
            result = "You win!"
        elif player_total > comp_total:
            result = "Computer wins!"
        else:
            result = "It's a tie!"
        messagebox.showinfo("Game Over", f"{reason}\n\nYour total: {player_total}\nComputer total: {comp_total}\n\n{result}")
        self.root.destroy()


# ---------- RUN ----------
if __name__ == "__main__":
    root = tk.Tk()
    game = BurntCarrotGame(root)
    root.mainloop()