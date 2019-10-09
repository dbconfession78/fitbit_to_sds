const FormData = require('form-data');
const fetch = require('node-fetch');
const baseURL = 'https://staging.osipi.com/api/v1/Tenants/1f11c599-be17-4812-a72f-00921b7716df/Namespaces/EmergingTech/';
const aqiDataAPI = require('./aqi_data');

const dataFromAPI = aqiDataAPI.returnData();
let counter = 0;

// Create form data for obtaining an access token.
const formData = new FormData();
formData.append('grant_type', 'client_credentials');
formData.append('client_id', 'b156af59-7385-4eca-b980-64c99b5b5b57');
formData.append('client_secret', 'dT+4abYS06WNXsrxCCeDfOds1vpXunFTAvwtlOp0MZM=');

// Obtain the token for access
const tokenURL = 'https://staging.osipi.com/identity/connect/token';
let accessToken = '';

// Fetch the token and assign it!
fetch(tokenURL, { method: 'POST', body: formData}).then(res => res.json())
.then(body => {
    accessToken = body.access_token;

    // Fetch and write data!
    const aqiData = [
        {...dataFromAPI[counter++] }
    ];
    console.log(aqiData);
    // Construct the options and perform fetch.
    const authString = "bearer " + accessToken;
    let options = {
        method: 'POST',
        body: JSON.stringify(aqiData),
        headers: {
            "Authorization": authString
        }
    };

    fetch(baseURL + 'Streams/aqistream/Data', options)
    .then(body => {
        // console.log(body);
    })
    .catch(err => console.log(err))


    setInterval(() => {
        const newData = [
            dataFromAPI[counter++]
        ];
        options.body = JSON.stringify(newData);
        // console.log(options);
        fetch(baseURL + 'Streams/aqistream/Data', options)
        .then(body => {
            // console.log(body);
        })
        .catch(err => console.log(err));
    }, 1000);

});