import http from 'k6/http';
import { check, sleep } from 'k6';

// ==========================
// Test configuration
// ==========================
export const options = {
    vus: 1000,          // 1000 virtual users
    duration: '2m',    // run test for 2 minutes
    thresholds: {
        http_req_duration: ['p(95)<500'] // 95% of requests < 500ms
    }
};

// ==========================
// API endpoint and auth
// ==========================
const API_URL = 'http://localhost:8000/users';
const API_KEY = __ENV.API_KEY; // pass via environment variable

// ==========================
// Test script
// ==========================
export default function () {
    // POST a test user
    const payload = JSON.stringify({
        name: `User_${__VU}_${__ITER}`,
        email: `user_${__VU}_${__ITER}@example.com`,
        age: 20 + (__ITER % 50)
    });

    const params = {
        headers: {
            'Content-Type': 'application/json',
            'X-API-Key': API_KEY
        }
    };

    const res = http.post(API_URL, payload, params);

    check(res, {
        'status is 200': (r) => r.status === 200,
    });

    // Optional sleep to simulate user think time
    sleep(0.05); // 50ms
}
