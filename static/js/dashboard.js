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
