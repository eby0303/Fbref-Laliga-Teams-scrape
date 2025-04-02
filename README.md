# ⚽ LaLiga Data Scraper & Dashboard  

## 📌 Overview  
This Streamlit web app automates the scraping of LaLiga teams' data from [FBref](https://fbref.com/). The app allows users to select a team, season, and specific statistical tables (e.g., defense, possession, pass types, etc.). The scraped data is then processed, stored in MongoDB, and displayed on the dashboard for easy access and analysis.  

## 🚀 Features  
- **Automated Scraping:** Fetch LaLiga team data for any season from FBref.  
- **Customizable Selection:** Choose the team, season, and desired statistical tables.  
- **Preprocessing:** Basic data cleaning before storing in MongoDB.  
- **Data Storage:** Saves scraped data in a MongoDB database.  
- **Interactive Dashboard:** View and analyze team stats directly on the Streamlit app.  

## 🛠️ Tech Stack  
- **Frontend:** [Streamlit](https://streamlit.io/)  
- **Backend:** Python (Requests, BeautifulSoup)  
- **Database:** MongoDB  
- **Data Processing:** Pandas  

## 🔧 Installation  

### 1️⃣ Clone the Repository  
```bash
git clone https://github.com/yourusername/laliga-fbref-scraper.git
cd laliga-fbref-scraper
```

### 2️⃣ Install Dependencies  
```bash
pip install -r requirements.txt
```

### 3️⃣ Set Up MongoDB  
Ensure you have MongoDB installed and running. Update the MongoDB connection string in the project if needed.

### 4️⃣ Run the Streamlit App  
```bash
streamlit run app.py
```

## 🖥️ Usage  
1. Open the Streamlit app in your browser.  
2. Select a **LaLiga team** and **season** from the dropdown menus.  
3. Choose the statistical tables you want to scrape.  
4. Click **Scrape Data** to fetch and store the data.  
5. View the scraped data directly in the dashboard.  

## 🏗️ Future Enhancements  
- Add visualization charts for better insights.  
- Implement caching for faster performance.  
- Expand to other leagues besides LaLiga.  

## 🤝 Contributing  
Feel free to fork the repo and submit pull requests!  

## 📜 License  
MIT License  

---
