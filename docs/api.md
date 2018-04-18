
**Add Register**  
----  
  Receive a call detail record and added a register  
* **URL**  
  
  api/v1/add_register/  
  
* **Method:**  
  
  `POST`  
    
*  **URL Params**  
  
    None  
  
* **Data Params**  
    -   There are two call detailed record types: **Call Start Record** and **Call End Record**.  

        **Call Start Record:** 
        ```console
        { 
	       "id":[integer]  // Record unique identificator;
	       "type":[string]  // Indicate if it's a call "start" or "end" record; 
	       "timestamp":[string]  // The timestamp of when the event occured; 
	       "call_id":[integer]  // Unique for each call record pair; 
	       "source":[string]  // The subscriber phone number that originated the call; 
	       "destination":[string]  // The phone number receiving the call. 
	     } 
        ```
 
        **Call End Record:** 
         ```console
        { 
	       "id":[integer]  // Record unique identificator;
	       "type":[string]  // Indicate if it's a call "start" or "end" record; 
	       "timestamp":[string]  // The timestamp of when the event occured; 
	       "call_id":[integer]  // Unique for each call record pair; 
	     } 
        ```
 
  
* **Success Response:**  
  
  * **Code:** 201 <br />  
    **Content:**  
      
      * `timestamp` format YYYY-MM-DD HH:MM:SS'
      
      If **type = start** 
      ```console
       { 
	       "id":[integer], 
	       "type":"start",
	       "timestamp":[string],
	       "call_id":[integer],   
	       "source":[string], 
	       "destination":[string]
       } 
    ```

    if **type = end**
    ```console  
    {
       "id":[integer] 
       "type":"end",
       "timestamp":[string]
       "call_id":[integer]   
    }
* **Error Response:**  
  
  * **Code:** 400 Bad Request <br />  
    **Content:** 
    ```console
    {"id": "This field is required."} 
    {"type": "This field is required."}
    {"call_id": "This field is required."}
    {"error": "{source} and {destination} is required for this type"}
    
    
  OR  
  
  * **Code:** 500 Internal Server Error <br />  
    **Content:** `{"Already register exist with \"id\" "}`  
  
* **Sample Call:**
    
    **Call Start Record:**
    url: http://HOST/api/v1/add_register/
    ```console
    {
        "call_id": 71, "source": "99988526423",
        "timestamp": "2017-12-12T15:07:13Z", "destination": "9993468278",
        "id": 1, "type": "start"
    }
    ```
    
    **Call End Record:**
    url: http://HOST/api/v1/add_register/
    ```console
    {
        "call_id": 71,
        "timestamp": "2017-12-13T15:07:13Z",
        "id": 2, "type": "end"
    }
    ```


**Get Phone Bill**  
----  
  Return the summary of phone account for month/year
    
* **URL**  
  
  api/v1/get_phone_bill/  
  
* **Method:**  
  
  `GET`  
    
*  **URL Params**  
    Required:

    `source=[string]`
    
    Optional:
    
    `period=[string]` *format MM/YYYY*` 
  
* **Data Params**  
    None
 
  
* **Success Response:**  
  
  * **Code:** 200 <br />  
    **Content:**  
    ```
     {
        "source": "99988526423",
        "calls": [
            {
                "call_duration": "0h:4m:58s",
                "destination": "9993468278",
                "start_date": "12/12/2017",
                "start_time": "15:07:58",
                "price": "R$ 0.72"
            },
            {
                "call_duration": "24h:13m:43s",
                "destination": "9993468278",
                "start_date": "12/12/2017",
                "start_time": "21:57:13",
                "price": "R$ 86.94"
            }
        ],
        "period": "12/2017"
    }
    ```
    
    Or
    
    ```
    {
        'calls": [], "source": "99988526423"
    }
    ```
* **Error Response:**  
  
  * **Code:** 400 Bad Request <br />  
    **Content:** 
    ```console
    {"period": "The format field is MM/YYYY, please informe a valid month/year"}
    {"source": "this is a required field"}

* **Sample Call:**
    
    url: http://HOST/api/v1/get_phone_bill/?source=99988526423&period=03/2018
    ```console
    {
        "source": "99988526423",
        "calls": [
            {
                "destination": "9993468278",
                "start_date": "12/03/2018",
                "start_time": "15:07:13",
                "call_duration": "2h:3m:0s",
                "price": "R$ 11.43"
            }
        ],
        "period": "3/2018",
        "amount": 11.43
    }
    ```
