import http from "k6/http";
import { check } from "k6";
import encoding from 'k6/encoding';
import { uuidv4 } from 'https://jslib.k6.io/k6-utils/1.4.0/index.js';
import { textSummary } from 'https://jslib.k6.io/k6-summary/0.0.1/index.js';
import { htmlReport } from "https://raw.githubusercontent.com/benc-uk/k6-reporter/main/dist/bundle.js";

let rebuildApiHostName = "HALO URL";
let testFilePath = "PATH TO FILE";

const file = open(testFilePath, "b");
const username = 'USERNAME';
const password = 'PASSWORD';

export const options = {
  vus:10,
  duration: '1m',
  insecureSkipTLSVerify: true,
};

export default function() {
	const credentials = `${username}:${password}`;
    const fileName = `${uuidv4()}${file.name}`
    const data = {
        file: http.file(file, fileName)
    };

    const encodedCredentials = encoding.b64encode(credentials);
    const params = {
	  headers: {
	    Authorization: `Basic ${encodedCredentials}`,
	  },
	  timeout: "60s"
    };
	
    const res = http.post(`${rebuildApiHostName}/api/v3/cdr-file`, data, params);

    if (!check(res, {
        "Response is Ok" : (r) => r.status === 201
    }))
    {
        console.error(res.body());
    }
}

export function handleSummary(data) {
      return {
        'stdout': textSummary(data, { indent: ' ', enableColors: true}), 
        'result.html': htmlReport(data),
        './summary.json': JSON.stringify(data)
      }
  }
