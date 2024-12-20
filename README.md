# Air Quality Visualization Project

A full-stack application for visualizing air quality data. This project includes a backend service for data management and a frontend dashboard for interactive data visualization.

---

## **Project Architecture**
![Project Architecture](snapshots/image-5.png)
---

## **Technologies Used**

### **Frontend (Angular 19)**
- **Framework:** Angular 19 (LTS)
- **Features:** 
  - Interactive charts using a charting library (ngx-Echarts).
  - Modern Angular features like standalone components and signals.
- **Development Environment:** Node.js 22.11-alpine.

### **Backend (Flask)**
- **Framework:** Flask
- **APIs:** RESTful APIs with Flask-Smorest.
- **Documentation:** API documented using Swagger (OpenAPI 3.0.3).
- **Database Interaction:** PyMongo.
- **Environment Variables:** Configured via `.env` file.
- **Unit Testing:** Pytest for unit testing.

### **Database (MongoDB)**
- **Type:** NoSQL Database.
- **Indexes:** Optimized for fast data retrieval using compound indexes.
- **Data Model:** Stores time-series air quality data.

### **Dockerization**
- **Container Orchestration:** Docker Compose.
- **Services:**
  - **MongoDB** for data storage.
  - **Backend** for API endpoints.
  - **Frontend** for user interaction.
- **Development Workflow:** Live reload using volume binding in containers.

---

## **API Documentation**

The API is documented using **Swagger**. You can access the interactive API documentation at:
```
http://localhost:5000/swagger-ui
```
Or simply navigate to the root URL of the backend API and it will redirect you to the Swagger UI page.
```
http://localhost:5000
```

Here are some snapshots of the API documentation:
![API docs snapshot 1](snapshots/image.png)
![API docs snapshot 2](snapshots/image-1.png)
---

## **Getting Started**

### **Setup**

1. **Clone the Repository**
   ```bash
   git clone https://github.com/your-repo-url.git
   cd air-quality-visualization
   ```

2. **Environment Variables**
   Find `.env` file in the root directory with the following content, and feel free to modify as per your requirements.
   ```env
   FLASK_ENV=development
   FLASK_DEBUG=1
   FLASK_APP=run.py
   FLASK_PORT=5000

   DASHBOARD_PORT=3000

   MONGO_HOST=mongo
   MONGO_PORT=27017
   MONGO_DB_NAME=air_quality
   MONGO_USERNAME=root
   MONGO_PASSWORD=my-pass
   MONGO_AUTH_SOURCE=admin
   ```

---

### **Run the Project**

1. **Build and Start Services**
   ```bash
   docker-compose up --build
   ```

2. **Access the Application**
   - **Backend API:** [http://localhost:5000](http://localhost:5000)
   - **Frontend Dashboard:** [http://localhost:3000](http://localhost:3000)

3. **Run Backend Unit Tests 'Optional'**
   - Get into backend folder and run the following command on terminal.
   - Make sure the packages in requirements_test.txt are installed.
   ```
      pytest tests/
   ```
---

## **How to Use**

### **Frontend Dashboard**

#### **Interactive Dashboard**
- Navigate to the **Dashboard**: [http://localhost:3000](http://localhost:3000).
- **Select Parameters:** Use the dropdown to select air quality parameters (e.g., CO, Benzene).
- **Filter Data:** Use the date range picker to filter data.

#### **Sample Snapshots**
![Line chart for all data in time range](snapshots/image-2.png)
![Bar chart for all data in time range](snapshots/image-3.png)
![Line chart for data filtered by parameter and time range](snapshots/image-4.png)

### **API Endpoints**

#### **Available Endpoints**
| Endpoint                        | Method | Description                                    |
|---------------------------------|--------|------------------------------------------------|
| `/api/air-quality`                  | `GET`  | Fetch api/air quality data for a date range.       |
| `/api/air-quality/paramters`        | `GET`  | Fetch data for a specific parameters           |
| `/api/air-quality/ingest_data`      | `POST` | Bulk upload air quality data via CSV.          |

#### **Request Example**
```bash
curl -X 'GET' "http://localhost:5000/api/air-quality?start_date=20-10-2004&end_date=30-10-2004" \ 
    -H 'accept: application/json'
```

#### **Response Example**
```json
[
    {
        "timestamp": "2023-01-01T00:00:00",
        "CO_GT": 1.2,
        "PT08_S1_CO": 1000,
        "NMHC_GT": 200,
        "C6H6_GT": 10,
        "PT08_S2_NMHC": 1000,
        "NOx_GT": 100,
        "PT08_S3_NOx": 1000,
        "NO2_GT": 100,
        "PT08_S4_NO2": 1000,
        "PT08_S5_O3": 1000,
        "T": 20,
        "RH": 50,
        "AH": 1
    },
    ...
]
```

**If we are filtering by specific parameters the reponse will be like:**
```json
[
    {
        "timestamp": "2023-01-01T00:00:00",
        "NMHC_GT": 1.2,
        "C6H6_GT": 1000,
    },
    ...
]
```

### **Data Ingestion**
#### **Upload Data via CSV**
- Upload air quality data in bulk using the `/api/air-quality/ingest_data` endpoint.
- Use the Swagger UI for easy data upload.
- **CSV File:** Sample CSV file is available at `backend/dataset/AirQualityUCI.csv`.

---

## **Acknowledgments**

- **Frontend Design:** Leveraging Angular 19 with advanced features.
- **Backend API:** Flask-Smorest for seamless API management.
- **Database:** MongoDB for efficient data handling.
- **Docker:** Simplified deployment and scalability.

---

Let me know if you need any modifications or additional sections!
