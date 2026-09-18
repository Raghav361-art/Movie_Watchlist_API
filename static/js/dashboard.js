requireAuth();

const state = {
  search: "",
  genre: "",
  watched: "",
  sort: "",
  limit: 9,
  offset: 0,
  editingId: null,
};

function currentUserId() {
  const token = API.token();
  if (!token) return null;
  try {
    const payload = JSON.parse(atob(token.split(".")[1]));
    return parseInt(payload.user_id, 10);
  } catch (e) {
    return null;
  }
}

// ---------------------------------------------------------------- elements
const reel = document.getElementById("reel");
const emptyState = document.getElementById("empty-state");
const resultCount = document.getElementById("result-count");
const pagination = document.getElementById("pagination");
const searchInput = document.getElementById("search-input");
const genreSelect = document.getElementById("genre-select");
const sortSelect = document.getElementById("sort-select");
const watchedToggle = document.getElementById("watched-toggle");
const logoutBtn = document.getElementById("logout-btn");
const addBtn = document.getElementById("add-movie-btn");
const emptyAddBtn = document.getElementById("empty-add-btn");

const modalBackdrop = document.getElementById("movie-modal");
const modalTitle = document.getElementById("modal-title");
const movieForm = document.getElementById("movie-form");
const modalError = document.getElementById("modal-error");
const cancelModalBtn = document.getElementById("cancel-modal");
const movieSearch = document.getElementById("movie-search");
const movieSearchInput = document.getElementById("movie-search-input");
const movieSearchResults = document.getElementById("movie-search-results");

let movieSearchDebounce;
let movieSearchController = null;
let movieSearchItems = [];
let movieSearchRequestId = 0;

movieSearchInput.addEventListener("input", () => {
  clearTimeout(movieSearchDebounce);
  movieSearchRequestId += 1;

  const query = movieSearchInput.value.trim();

  if (query.length < 2) {
    if (movieSearchController) movieSearchController.abort();
    movieSearchResults.innerHTML = "";
    movieSearchResults.classList.remove("open");
    movieSearchInput.setAttribute("aria-expanded", "false");
    return;
  }

  movieSearchDebounce = setTimeout(() => {
    searchMovies(query);
  }, 350);
});
async function searchMovies(query) {
  if (movieSearchController) {
    movieSearchController.abort();
  }

  const requestId = movieSearchRequestId;
  movieSearchController = new AbortController();

  movieSearchResults.innerHTML = `
    <div class="movie-search-empty">
      Searching...
    </div>
  `;

  movieSearchResults.classList.add("open");
  movieSearchInput.setAttribute("aria-expanded", "true");

  try {
    const response = await fetch(
      `/movies/search?query=${encodeURIComponent(query)}`,
      {
        headers: {
          Authorization: `Bearer ${API.token()}`
        },
        signal: movieSearchController.signal
      }
    );

    if (!response.ok) {
      throw new Error("Movie search failed");
    }

    const movies = await response.json();

    if (requestId !== movieSearchRequestId) return;
    renderMovieSearchResults(movies);

  } catch (err) {
    if (err.name === "AbortError" || requestId !== movieSearchRequestId) {
      return;
    }

    movieSearchResults.innerHTML = `
      <div class="movie-search-empty">
        Couldn't search for movies. Please try again.
      </div>
    `;
  }
}
function renderMovieSearchResults(movies) {
  movieSearchResults.innerHTML = "";
  movieSearchItems = Array.isArray(movies) ? movies : [];

  if (movieSearchItems.length === 0) {
    movieSearchResults.innerHTML = `
      <div class="movie-search-empty">
        No movies found.
      </div>
    `;

    movieSearchResults.classList.add("open");
    return;
  }

  movieSearchItems.forEach((movie, index) => {
    const result = document.createElement("div");
    result.className = "movie-search-result";
    result.setAttribute("role", "option");

    const releaseDate = movie.release_year || "";
    const releaseYear = releaseDate ? String(releaseDate).slice(0, 4) : "Unknown year";
    const rating = movie.rating === null || movie.rating === undefined
      ? "Not rated"
      : String(movie.rating);
    const director = movie.director || "Director unavailable";
    const genres = movie.genres || "Genre unavailable";

    result.innerHTML = `
      <div class="movie-search-info">
        <div class="movie-search-title">
          ${escapeHtml(movie.title || "Untitled")}
        </div>

        <div class="movie-search-meta">
          <span>${escapeHtml(releaseYear)}</span>
          <span>${escapeHtml(director)}</span>
          <span>${escapeHtml(genres)}</span>
          <span>Rating: ${escapeHtml(rating)}</span>
        </div>
      </div>

      <button
        class="btn btn-primary btn-sm movie-search-add"
        data-result-index="${index}"
        type="button"
      >
        Add
      </button>
    `;

    movieSearchResults.appendChild(result);
  });

  movieSearchResults.classList.add("open");
  movieSearchInput.setAttribute("aria-expanded", "true");
}
movieSearchResults.addEventListener("click", async (e) => {
  const button = e.target.closest(".movie-search-add");

  if (!button) return;

  const movie = movieSearchItems[Number(button.dataset.resultIndex)];
  if (!movie || button.disabled) return;

  button.disabled = true;
  button.textContent = "Adding...";

  try {
    await API.createMovie({
      title: movie.title || "Untitled",
      director: movie.director || "Unknown",
      genre: movie.genres || "Other",
      release_year: parseInt(String(movie.release_year || "").slice(0, 4), 10),
      rating: Number.isFinite(Number(movie.rating)) && Number(movie.rating) <= 10
        ? Number(movie.rating)
        : null,
      watched: false
    });

    showToast("Added to your watchlist.");

    button.textContent = "Added";

    loadMovies();

  } catch (err) {
    button.disabled = false;
    button.textContent = "Add";

    showToast(
      err.message || "Couldn't add movie.",
      true
    );
  }
});

document.addEventListener("click", (e) => {
  if (!movieSearch.contains(e.target)) {
    movieSearchResults.classList.remove("open");
    movieSearchInput.setAttribute("aria-expanded", "false");
  }
});

// ---------------------------------------------------------------- rendering
function starRow(rating) {
  if (rating === null || rating === undefined) return "Not rated";
  return `${rating} / 10`;
}

function ticketTemplate(entry) {
  const movie = entry.Movie;
  const likeCount = entry.likeCount;
  const liked = entry.liked;
  const isOwner = movie.user_id === currentUserId();

  const el = document.createElement("article");
  el.className = "ticket";
  el.innerHTML = `
    <div class="ticket-main">
      <div class="ticket-title-row">
        <div class="ticket-title">${escapeHtml(movie.title)}</div>
        <div class="ticket-year">${movie.release_year}</div>
      </div>
      <div class="ticket-meta">
        <span class="pill">${escapeHtml(movie.genre)}</span>
        <span class="pill ${movie.watched ? "pill-watched" : "pill-unwatched"}">
          ${movie.watched ? "Watched" : "Queued"}
        </span>
      </div>
      <div class="ticket-director">Directed by ${escapeHtml(movie.director)}</div>
      <div class="ticket-rating">★ ${starRow(movie.rating)}</div>
    </div>
    <div class="ticket-stub">
      <button class="like-btn ${liked ? "liked" : ""}" data-action="like" data-id="${movie.id}" title="Like this movie">
        <svg viewBox="0 0 24 24" fill="${liked ? "currentColor" : "none"}" stroke="currentColor" stroke-width="1.6">
          <path d="M12 21s-7.2-4.55-9.9-9A5.5 5.5 0 0 1 12 6a5.5 5.5 0 0 1 9.9 6c-2.7 4.45-9.9 9-9.9 9z"/>
        </svg>
        ${likeCount}
      </button>
      ${
        isOwner
          ? `<div class="stub-actions">
              <button class="icon-btn" data-action="edit" data-id="${movie.id}">Edit</button>
              <button class="icon-btn danger" data-action="delete" data-id="${movie.id}">Delete</button>
            </div>`
          : ""
      }
    </div>
  `;
  return el;
}

function escapeHtml(str) {
  const div = document.createElement("div");
  div.textContent = str;
  return div.innerHTML;
}

async function loadMovies() {
  reel.innerHTML = Array.from({ length: 3 })
    .map(() => `<div class="skeleton"></div>`)
    .join("");
  emptyState.classList.add("hidden");

  try {
    const results = await API.listMovies({
      search: state.search,
      genre: state.genre,
      watched: state.watched,
      sort: state.sort,
      limit: state.limit,
      offset: state.offset,
    });

    reel.innerHTML = "";

    if (!results || results.length === 0) {
      emptyState.classList.remove("hidden");
      resultCount.textContent = "";
      renderPagination(0);
      return;
    }

    results.forEach((entry) => reel.appendChild(ticketTemplate(entry)));
    resultCount.textContent = `${results.length} shown`;
    renderPagination(results.length);
  } catch (err) {
    showToast(err.message || "Couldn't load your watchlist.", true);
    reel.innerHTML = "";
    emptyState.classList.remove("hidden");
  }
}

function renderPagination(currentCount) {
  pagination.innerHTML = "";

  const prevBtn = document.createElement("button");
  prevBtn.className = "btn btn-sm";
  prevBtn.textContent = "← Newer";
  prevBtn.disabled = state.offset === 0;
  prevBtn.addEventListener("click", () => {
    state.offset = Math.max(0, state.offset - state.limit);
    loadMovies();
  });

  const nextBtn = document.createElement("button");
  nextBtn.className = "btn btn-sm";
  nextBtn.textContent = "Older →";
  nextBtn.disabled = currentCount < state.limit;
  nextBtn.addEventListener("click", () => {
    state.offset += state.limit;
    loadMovies();
  });

  pagination.appendChild(prevBtn);
  pagination.appendChild(nextBtn);
}

// ---------------------------------------------------------------- filters
let searchDebounce;
searchInput.addEventListener("input", () => {
  clearTimeout(searchDebounce);
  searchDebounce = setTimeout(() => {
    state.search = searchInput.value.trim();
    state.offset = 0;
    loadMovies();
  }, 350);
});

genreSelect.addEventListener("change", () => {
  state.genre = genreSelect.value;
  state.offset = 0;
  loadMovies();
});

sortSelect.addEventListener("change", () => {
  state.sort = sortSelect.value;
  state.offset = 0;
  loadMovies();
});

watchedToggle.addEventListener("change", () => {
  state.watched = watchedToggle.checked ? "true" : "";
  state.offset = 0;
  loadMovies();
});

// ---------------------------------------------------------------- add/edit modal
function openModal(entry = null) {
  modalError.classList.remove("show");
  movieForm.reset();

  if (entry) {
    state.editingId = entry.id;
    modalTitle.textContent = "Edit movie";
    document.getElementById("m-title").value = entry.title;
    document.getElementById("m-director").value = entry.director;
    document.getElementById("m-genre").value = entry.genre;
    document.getElementById("m-year").value = entry.release_year;
    document.getElementById("m-rating").value = entry.rating ?? "";
    document.getElementById("m-watched").checked = entry.watched;
  } else {
    state.editingId = null;
    modalTitle.textContent = "Add a movie";
  }

  modalBackdrop.classList.add("open");
}

function closeModal() {
  modalBackdrop.classList.remove("open");
}

addBtn.addEventListener("click", () => openModal());
emptyAddBtn.addEventListener("click", () => openModal());
cancelModalBtn.addEventListener("click", closeModal);
modalBackdrop.addEventListener("click", (e) => {
  if (e.target === modalBackdrop) closeModal();
});

movieForm.addEventListener("submit", async (e) => {
  e.preventDefault();
  modalError.classList.remove("show");

  const payload = {
    title: document.getElementById("m-title").value.trim(),
    director: document.getElementById("m-director").value.trim(),
    genre: document.getElementById("m-genre").value.trim(),
    release_year: parseInt(document.getElementById("m-year").value, 10),
    rating: parseInt(document.getElementById("m-rating").value, 10),
    watched: document.getElementById("m-watched").checked,
  };

  const btn = movieForm.querySelector("button[type=submit]");
  btn.disabled = true;

  try {
    if (state.editingId) {
      await API.updateMovie(state.editingId, payload);
      showToast("Movie updated.");
    } else {
      await API.createMovie(payload);
      showToast("Added to your watchlist.");
    }
    closeModal();
    loadMovies();
  } catch (err) {
    modalError.textContent = err.message || "Something went wrong.";
    modalError.classList.add("show");
  } finally {
    btn.disabled = false;
  }
});

// ---------------------------------------------------------------- card actions (event delegation)
reel.addEventListener("click", async (e) => {
  const btn = e.target.closest("button[data-action]");
  if (!btn) return;
  const id = parseInt(btn.dataset.id, 10);
  const action = btn.dataset.action;

  if (action === "like") {
    const alreadyLiked = btn.classList.contains("liked");
    try {
      await API.vote(id, !alreadyLiked);
      loadMovies();
    } catch (err) {
      showToast(err.message || "Couldn't update your vote.", true);
    }
  }

  if (action === "edit") {
    try {
      const entry = await API.getMovie(id);
      openModal(entry.Movie);
    } catch (err) {
      showToast("Couldn't load that movie.", true);
    }
  }

  if (action === "delete") {
    if (!confirm("Remove this movie from your watchlist?")) return;
    try {
      await API.deleteMovie(id);
      showToast("Movie removed.");
      loadMovies();
    } catch (err) {
      showToast(err.message || "Couldn't delete that movie.", true);
    }
  }
});

// ---------------------------------------------------------------- logout
logoutBtn.addEventListener("click", () => {
  API.clearToken();
  window.location.href = "/";
});

loadMovies();
