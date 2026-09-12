document.addEventListener("DOMContentLoaded", () => {
  // If already logged in, skip straight to the dashboard.
  if (API.isLoggedIn()) {
    window.location.href = "/dashboard";
    return;
  }

  const tabs = document.querySelectorAll(".auth-tab");
  const forms = document.querySelectorAll(".auth-form");

  tabs.forEach((tab) => {
    tab.addEventListener("click", () => {
      tabs.forEach((t) => t.classList.remove("active"));
      forms.forEach((f) => f.classList.remove("active"));
      tab.classList.add("active");
      document.getElementById(tab.dataset.target).classList.add("active");
    });
  });

  // ---- Login ----
  const loginForm = document.getElementById("login-form");
  const loginError = document.getElementById("login-error");

  loginForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    loginError.classList.remove("show");
    const email = document.getElementById("login-email").value.trim();
    const password = document.getElementById("login-password").value;
    const btn = loginForm.querySelector("button[type=submit]");
    btn.disabled = true;

    try {
      const data = await API.login(email, password);
      API.setToken(data.access_token);
      window.location.href = "/dashboard";
    } catch (err) {
      loginError.textContent = err.message || "Wrong credentials. Try again.";
      loginError.classList.add("show");
    } finally {
      btn.disabled = false;
    }
  });

  // ---- Register ----
  const registerForm = document.getElementById("register-form");
  const registerError = document.getElementById("register-error");

  registerForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    registerError.classList.remove("show");
    const email = document.getElementById("register-email").value.trim();
    const password = document.getElementById("register-password").value;
    const confirm = document.getElementById("register-confirm").value;
    const btn = registerForm.querySelector("button[type=submit]");

    if (password !== confirm) {
      registerError.textContent = "Passwords don't match.";
      registerError.classList.add("show");
      return;
    }

    btn.disabled = true;
    try {
      await API.register(email, password);
      // Auto-login right after registering.
      const data = await API.login(email, password);
      API.setToken(data.access_token);
      window.location.href = "/dashboard";
    } catch (err) {
      registerError.textContent =
        err.status === 409 ? "An account with that email already exists." : err.message;
      registerError.classList.add("show");
    } finally {
      btn.disabled = false;
    }
  });
});
