import time
import random
from playwright.sync_api import sync_playwright
from ai_model import Predictor
from gui import DraggableWindow
import threading

class BloxluckAI:
    def __init__(self):
        self.predictor = Predictor("trained_model.h5")
        self.running = True
        self.ui = DraggableWindow()
        
    def scrape_outcomes(self):
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto("https://bloxluck.com")  # Target URL
            
            while self.running:
                outcome = page.query_selector(".result-text").inner_text()
                if outcome and (not self.predictor.history or outcome != self.predictor.history[-1]):
                    self.predictor.history.append(outcome)
                    self.update_predictions()
                    time.sleep(random.uniform(1.5, 3.5))
                    
    def update_predictions(self):
        prediction = self.predictor.predict_next()
        confidence = random.randint(65, 90)  # Simulated confidence
        self.ui.update_ui(prediction, confidence)
        
    def run(self):
        threading.Thread(target=self.scrape_outcomes, daemon=True).start()
        self.ui.mainloop()
        self.running = False

if __name__ == "__main__":
    ai = BloxluckAI()
    ai.run()
