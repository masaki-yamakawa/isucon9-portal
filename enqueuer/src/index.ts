import 'dotenv/config';
import fetch from 'node-fetch';

import { poll } from './poll';

const baseDomain = process.env.PORTAL_API_SERVER ? process.env.PORTAL_API_SERVER : "http://localhost:8001/";
const baseURL = `${baseDomain}internal/`;
const participateAt = process.env.PARTICIPATE_AT ? process.env.PARTICIPATE_AT : "2022-04-18";

console.log(`Enqueuer start. API server baseURL=${baseURL}, participateAt=${participateAt}`);

async function enqueue() {
  // console.log('Check benchmaker queue');

  const resServers = await fetch(`${baseURL}server/target/?participate_at=${participateAt}`);
  const servers = await resServers.json();

  for (const server of servers) {
    console.log('team_id=' + server.team_id + ", global_ip=" + server.global_ip);

    const resLatestJob = await fetch(`${baseURL}job/latest/?team_id=${server.team_id}`);
    const latestJob = await resLatestJob.json();
    // console.log('latestJobStatus=' + latestJob.status + ", " + JSON.stringify(latestJob));
    if (latestJob.status === 'waiting' || latestJob.status === 'running') {
      console.log(`Skip enqueue. team=${latestJob.team.name}, id=${latestJob.id}, status=${latestJob.status}`);
      continue;
    } else {
      console.log(`Execute enqueue. team=${latestJob.team.name}, id=${latestJob.id}, status=${latestJob.status}`);
      const body = { team_id: server.team_id };
      const options = {
        method: 'POST',
        body: JSON.stringify(body),
        headers: { 'Content-Type': 'application/json' },
      }
      const enqueueRes = await fetch(`${baseURL}job/enqueue/`, options);
      const enqueueResult = await enqueueRes.json();
      console.log('enqueueRes=' + JSON.stringify(enqueueResult));
    }
  }
}

poll(enqueue, 10000);
