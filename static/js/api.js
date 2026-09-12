/* Shared API helper for the Movie Watchlist frontend.
   Talks to the FastAPI backend defined in app/routers/*.py */

const API = {
  base: "", // same-origin; change to "http://localhost:8000" if serving templates elsewhere

  token() {
    return localStorage.getItem("watchlist_token");
  },

  setToken(token) {
    localStorage.setItem("watchlist_token", token);
  },

  clearToken() {
    localStorage.removeItem("watchlist_token");
  },

  isLoggedIn() {
    return !!this.token();
  },

  async request(path, { method = "GET", body, form = false, auth = true } = {}) {
    const headers = {};
    if (auth && this.token()) {
      headers["Authorization"] = `Bearer ${this.token()}`;
    }

    let payload = body;
    if (body && !form) {
      headers["Content-Type"] = "application/json";
      payload = JSON.stringify(body);
    }

    const res = await fetch(`${this.base}${path}`, {
      method,
      headers,
      body: payload,
    });

    if (res.status === 204) return null;

    let data = null;
    try {
      data = await res.json();
    } catch (e) {
      /* no body */
    }

    if (!res.ok) {
      const message =
        (data && (data.detail || data.message)) || `Request failed (${res.status})`;
      const err = new Error(typeof message === "string" ? message : JSON.stringify(message));
      err.status = res.status;
      throw err;
    }

    return data;
  },

  // ---- Auth ----
  login(email, password) {
    const form = new URLSearchParams();
    form.append("username", email);
    form.append("password", password);
    return this.request("/login", { method: "POST", body: form, form: true, auth: false });
  },

  register(email, password) {
    return this.request("/user/", {
      method: "POST",
      body: { email, password },
      auth: false,
    });
  },

  // ---- Movies ----
  listMovies({ search = "", genre = "", watched = null, sort = "", limit = 12, offset = 0 } = {}) {
    const params = new URLSearchParams();
    if (search) params.set("search", search);
    if (genre) params.set("genre", genre);
    if (watched !== null && watched !== "") params.set("watched", watched);
    if (sort) params.set("sort", sort);
    params.set("limit", limit);
    params.set("offset", offset);
    return this.request(`/movies/?${params.toString()}`);
  },

  getMovie(id) {
    return this.request(`/movies/${id}`, { auth: false });
  },

  createMovie(movie) {
    // backend expects a list of movies
    return this.request("/movies/", { method: "POST", body: [movie] });
  },

  updateMovie(id, movie) {
    return this.request(`/movies/${id}`, { method: "PUT", body: movie });
  },

  deleteMovie(id) {
    return this.request(`/movies/${id}`, { method: "DELETE" });
  },

  vote(movieId, dir) {
    return this.request("/vote/", { method: "POST", body: { movie_id: movieId, dir } });
  },
};

function showToast(message, isError = false) {
  const toast = document.getElementById("toast");
  if (!toast) return;
  toast.textContent = message;
  toast.classList.toggle("error", isError);
  toast.classList.add("show");
  clearTimeout(showToast._t);
  showToast._t = setTimeout(() => toast.classList.remove("show"), 3200);
}

function requireAuth() {
  if (!API.isLoggedIn()) {
    window.location.href = "/";
  }
}
