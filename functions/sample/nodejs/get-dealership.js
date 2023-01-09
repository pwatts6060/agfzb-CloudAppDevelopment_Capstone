 /**
  *
  * main() will be run when you invoke this action
  *
  * @param Cloud Functions actions accept a single parameter, which must be a JSON object.
  *
  * @return The output of this action, which must be a JSON object.
  *
  */
 function main(params) {
	return new Promise(function (resolve, reject) {
		const { CloudantV1 } = require('@ibm-cloud/cloudant');
		const { IamAuthenticator } = require('ibm-cloud-sdk-core');
		const authenticator = new IamAuthenticator({ apikey: "C8MMcmyzCvtx4ir7Q1hgcaXIIczBkURAScRGys3Gc7G3" })
		const cloudant = CloudantV1.newInstance({
			authenticator: authenticator
		});
        cloudant.setServiceUrl("https://apikey-v2-2sd76a0jxkyktdflxbypp5n2u2iq7zjx60nn1ja9w7mm:b4e172bb6be98e1d138d32e666876922@76ff4ea4-f27a-47e5-8087-9f43fa42f5e3-bluemix.cloudantnosqldb.appdomain.cloud");
        if (params.st) {
			// return dealership with this state
			cloudant.postFind({db:'dealerships',selector:{st:params.st}})
			.then((response)=>{
			  let code = 200;
			  if (response.result.docs.length == 0) {
				  code = 404;
			  }
			  resolve({
				  statusCode: code,
				  headers: { 'Content-Type': 'application/json' },
				  body: response.result.docs
			  });
			}).catch((err)=>{
			  reject(err);
			})
		} else if (params.id) {
			id = parseInt(params.dealerId)
			// return dealership with this state
			cloudant.postFind({
			  db: 'dealerships',
			  selector: {
				id: parseInt(params.id)
			  }
			})
			.then((response)=>{
			  let code = 200;
			  if (response.result.docs.length == 0) {
				  code = 404;
			  }
			  resolve({
				  statusCode: code,
				  headers: { 'Content-Type': 'application/json' },
				  body: response.result.docs
			  });
			}).catch((err)=>{
			  reject(err);
			})
		} else {
			// return all documents
			cloudant.postAllDocs({ db: 'dealerships', includeDocs: true, limit: 10 })
			.then((response)=>{
			  let code = 200;
			  if (response.result.rows.length == 0) {
				  code = 404;
			  }
			  resolve({
				  statusCode: code,
				  headers: { 'Content-Type': 'application/json' },
				  body: response.result.rows
			  });
			}).catch((err)=>{
			  reject(err);
			})
	  }
	}
)}