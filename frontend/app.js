const API_BASE = "";

// Fetch con manejo de errores
async function api(path, opts = {}) {
  const url = API_BASE + path;
  const headers = { "Content-Type": "application/json" };
  const method = opts.method || "GET";
  const body = opts.body ? JSON.stringify(opts.body) : undefined;

  const res = await fetch(url, { method, headers, body });

  if (res.ok) {
    const ct = res.headers.get("content-type") || "";
    return ct.includes("application/json") ? res.json() : res.text();
  }

  // Intentar leer JSON de error
  let data;
  try { data = await res.json(); } catch { data = { error: await res.text() }; }

  // Si el backend dice que el alumno no existe, limpiar sesión y volver al login
  if (res.status === 404 && /student not found/i.test(data?.error || "")) {
    try { localStorage.removeItem("student"); } catch {}
    window.location.href = "index.html";
    throw new Error("Student not found → redirigiendo a login");
  }

  const err = new Error(`HTTP ${res.status}`);
  err.status = res.status;
  err.data = data;
  throw err;
}

// Session helpers
function setStudent(student) {
  localStorage.setItem("student", JSON.stringify(student));
}
function getStudent() {
  const raw = localStorage.getItem("student");
  if (!raw) {
    window.location.href = "index.html";
    throw new Error("sin sesión");
  }
  return JSON.parse(raw);
}
function logout() {
  localStorage.removeItem("student");
  // (opcional) avisar al backend
  fetch("/api/auth/logout", { method: "POST" }).finally(() => {
    window.location.href = "index.html";
  });
}
function hardReset() {
  localStorage.clear(); sessionStorage.clear();
  fetch("/api/dev/reset", { method: "POST" }).catch(()=>{}).finally(()=>location.href="index.html");
}

// AUTH
async function authRegister({ name, course, username, password }) {
  const s = await api("/api/auth/register", { method: "POST", body: { name, course, username, password } });
  setStudent(s);
  location.href = "menu.html";
}
async function authLogin({ username, password }) {
  const s = await api("/api/auth/login", { method: "POST", body: { username, password } });
  setStudent(s);
  location.href = "menu.html";
}

// Exponer helpers a la ventana por si los usas inline
window.logout = logout;
window.hardReset = hardReset;
window.authRegister = authRegister;
window.authLogin = authLogin;
window.getStudent = getStudent;
