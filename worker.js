// Lunas edge: static site from this repo, everything that belongs to the app
// proxied to the Railway service so the site and the app share one hostname
// (cookies, /v pages, badges, OAuth callbacks all stay on lunas.novesteria.com).
// Assets are matched first by the platform; this only runs when no file matches.
const APP_PATHS = ["/app", "/api", "/v", "/b", "/u", "/join", "/static", "/health"];

function isApp(pathname) {
  return APP_PATHS.some((p) => pathname === p || pathname.startsWith(p + "/"));
}

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    // Old name. The whole site moved to lunas.novesteria.com on 20 Sep 2026:
    // 301 for GET/HEAD so browsers and crawlers learn the move, 308 for the
    // rest so API clients keep method and body. /health stays local for probes.
    if (url.host === "aegis.novesteria.com" && url.pathname !== "/health") {
      url.host = "lunas.novesteria.com";
      const code = request.method === "GET" || request.method === "HEAD" ? 301 : 308;
      return Response.redirect(url.toString(), code);
    }
    if (isApp(url.pathname) && env.APP_ORIGIN) {
      const origin = new URL(env.APP_ORIGIN);
      const upstream = new URL(url.pathname + url.search, origin);
      const headers = new Headers(request.headers);
      headers.set("X-Forwarded-Host", url.host);
      headers.set("X-Forwarded-Proto", url.protocol.replace(":", ""));
      const init = { method: request.method, headers, redirect: "manual" };
      if (request.method !== "GET" && request.method !== "HEAD") init.body = request.body;
      return fetch(upstream.toString(), init);
    }
    return env.ASSETS.fetch(request);
  },
};
