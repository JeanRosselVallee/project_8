# Goals : 
- Deploy API Model to Google Cloud
	- Credit Score of a borrower's ability to repay debt
	- Returns the probability that a borrower repays a debt
- Deploy GUI as an App running on Streamlit Apps' server 
	- Access to API via REST requests
	- Help in decision-making to approve or reject a credit application

<img src="https://live.staticflickr.com/8277/29132289432_0eace56cf1_z.jpg">

# Context :
- There are 2 classes of borrowers depending on the probability to repay a debt
- The approval of the application relies on this probability

For more details, check this [presentation of the project](docs/Vallée_Jean_4_présentation_072024.pdf).

Try the app at [StreamLit](https://project8-dashboard.streamlit.app/)
- Re-boot app & server if stopped.

### Re-boot Instructions 
- BackEnd on GCP
	- [VM #1](https://console.cloud.google.com/compute/instancesDetail/zones/europe-west9-c/instances/6536832866304815511?project=ocr-p8-dashboard)
 		- Start/Resume 
		- SSH > "open in browser window"
  			- cd ~/project_8/shl/
			- ./launch_mlflow.sh
   		- Get External IP @ [VM Instances](https://console.cloud.google.com/compute/instances?project=ocr-p8-dashboard)
- Check BackEnd's response on local PC
	- PowerShell terminal (update IP)
		```
		Invoke-RestMethod -Method Post -Uri "http://<IP>:5677/invocations" `
		 -ContentType "application/json" `
		 -Body '{"dataframe_split": {"columns":["CODE_GENDER_M","EXT_SOURCE_3","EXT_SOURCE_2","NAME_EDUCATION_TYPE_Secondary_or_secondary_special","NAME_EDUCATION_TYPE_Higher_education","NAME_CONTRACT_TYPE_Cash_loans","NAME_INCOME_TYPE_Working"],"index":[2011],"data":[[0,0.5989262183,0.1461036398,1,0,1,1]]}}'
		```
- Check GCP [Billing](https://console.cloud.google.com/billing/0136C7-720E0A-C5CEC6/reports;credits=NONE;negotiatedSavings=false?project=ocr-p8-dashboard)
- FontEnd on StreamLit
	- Login with GitHub
 	- Go to [apps list](https://share.streamlit.io/)
  	- 3-dots > Reboot
- Check [app](https://project8-dashboard.streamlit.app/)

