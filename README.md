# 🍲 Foodie AI: Your Recipe & Cooking Assistant

Foodie AI is a Streamlit web app that answers your food and recipe questions using your own local recipe dataset and an AI model. It can:
- Instantly search and display recipes from your local dataset (`full_format_recipes.json`)
- Fall back to an AI model (Ollama/Deepseek) for general food questions or if a recipe is not found

## Features
- **Local Recipe Search:** Fast, private, and accurate answers from your own recipe collection
- **AI-Powered Answers:** Get creative or general food/cooking advice from an LLM
- **Simple UI:** Just type your question and get an answer!

## Running the Project (Step by Step)

1. **Clone the repository:**
   ```powershell
   git clone https://github.com/SeifSlimen/Custom-food-AI.git
   cd Custom-food-AI
   ```
2. **Install Python dependencies:**
   ```powershell
   pip install -r requirements.txt
   ```
3. **Prepare your recipe dataset:**
   - Place your `full_format_recipes.json` in the `2/` directory (see sample structure).
   - (Optional) Use `download_recipes.py` to fetch a sample dataset.
4. **Install and start Ollama:**
   - Download and install Ollama from [https://ollama.com/](https://ollama.com/)
   - Open a terminal and pull the Deepseek model:
     ```powershell
     ollama pull deepseek-r1:7b
     ```
   - Start the model (in a separate terminal if you want):
     ```powershell
     ollama run deepseek-r1:7b
     ```
5. **Run the Streamlit app:**
   ```powershell
   streamlit run app.py
   ```
6. **Open your browser:**
   - Go to the local URL shown by Streamlit (usually http://localhost:8501)

> **Note:** The app uses the Deepseek model via Ollama as specified in the code. Make sure Ollama is running and the model is available before starting the app.

## File Structure
```
app.py                  # Main Streamlit app
2/full_format_recipes.json  # Your recipe dataset (JSON)
2/recipe.py, 2/utils.py     # Recipe extraction and helpers
2/epi_r.csv                # (Optional) Tabular recipe data
```

## Example Usage
- "How do I make lasagna?"
- "Give me a vegan dessert recipe."
- "What are some tips for baking bread?"

## Credits
- Built with [Streamlit](https://streamlit.io/) and [Ollama](https://ollama.com/)
- Recipe data: [Epicurious](https://www.epicurious.com/) and others

## License
MIT
