export default {
  async fetch(request, env) {
    const url = new URL(request.url);

    if (url.pathname === "/chat") {
      // Save current timestamp in KV
      await env.LAST_REQUEST_KV.put("last_request", Date.now().toString());

      // Check Pod status
      const statusResp = await fetch(`https://api.runpod.io/pods/${env.RUNPOD_POD_ID}`, {
        headers: { "Authorization": `Bearer ${env.RUNPOD_API_KEY}` }
      });
      const status = await statusResp.json();

      if (status.status !== "RUNNING") {
        await fetch(`https://api.runpod.io/pods/${env.RUNPOD_POD_ID}/start`, {
          method: "POST",
          headers: { "Authorization": `Bearer ${env.RUNPOD_API_KEY}` }
        });
        return new Response(JSON.stringify({ message: "Pod starting, try again in ~60s" }), { status: 202 });
      }

      // Forward request to vLLM
      const body = await request.json();
      return fetch(`http://${env.RUNPOD_POD_IP}:8000/v1/chat/completions`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body)
      });
    }

    return new Response("Not found", { status: 404 });
  }
};