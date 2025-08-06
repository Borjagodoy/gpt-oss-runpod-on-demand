export default {
  async scheduled(event, env, ctx) {
    const lastRequest = parseInt(await env.LAST_REQUEST_KV.get("last_request")) || Date.now();
    const diffMinutes = (Date.now() - lastRequest) / 1000 / 60;

    if (diffMinutes > parseInt(env.INACTIVITY_LIMIT_MINUTES || "10")) {
      await fetch(`https://api.runpod.io/pods/${env.RUNPOD_POD_ID}/stop`, {
        method: "POST",
        headers: { "Authorization": `Bearer ${env.RUNPOD_API_KEY}` }
      });
    }
  }
};