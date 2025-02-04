### **CS2 Round Handicap Edge Calculator: Predicting Round Handicap in CS2 Matches**

#### **Overview**
CS2 Round Handicap Edge Calculator is a sports betting project aimed at analyzing historical Counter-Strike 2 match data to optimize round handicap predictions. The project scrapes match data from HLTV, extracts detailed round-by-round information from demos, and applies statistical and machine learning techniques to determine the probability of different round handicaps.  

#### **Features**
- Scrapes historical match data from **HLTV**.  
- Parses demo files to extract **round-by-round performance metrics**.  
- Computes **round handicap probabilities** for more informed betting.  

#### **How It Works**
1. **Data Collection**:  
   - Scrape match results and statistics from HLTV.  
   - Extract demo data to analyze team performance at a granular level.  

2. **Data Processing**:  
   - Convert raw match data into structured datasets.  
   - Compute key performance indicators (KPIs) such as **round wins, economy trends, weapon usage, and clutch statistics**.  

3. **Handicap Prediction**:  
   - Train models to estimate the **probability of specific round handicaps** (e.g., a team winning by a margin of 2, 3, or more rounds).  
   - Use statistical analysis and machine learning to detect betting inefficiencies.  

#### **Potential Applications**
- **Creating more accurate betting models** for CS2 match handicaps.  
- **Identifying profitable betting opportunities** using predictive analytics.  
- **Enhancing esports betting strategies** with real-time round-based probabilities.  

#### **Setup Instructions**
1. Clone the repository:  
   ```bash
   git clone https://github.com/hitansh1299/CS2-Round-Handicap-Edge-Calculator.git
   ```
2. Install dependencies:  
   ```bash
   pip install -r requirements.txt
   ```
3. Run the scraper:  
   ```bash
   python scrape_hltv.py
   ```
4. Process the demo data:  
   ```bash
   python parse_demos.py
   ```
5. Generate predictions:  
   ```bash
   python predict_handicap.py
   ```

#### **Roadmap**
- ✅ **Scraping HLTV match data**  
- 🚧 **Extracting demo statistics**  
- 🚧 **Building predictive models for round handicap probabilities**  
- 🚧 **Developing a user-friendly betting dashboard**  

#### **Contributing**
If you're interested in contributing, feel free to submit a pull request or open an issue!  

#### **License**
MIT License  