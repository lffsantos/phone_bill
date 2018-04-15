
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
