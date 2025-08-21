const { test, expect } = require('@playwright/test');

function randomUser() {
  const s = Date.now().toString().slice(-6);
  return { name: `QA Bot ${s}`, course: '2do', username: `qa_${s}`, password: '1234' };
}

test('flujo completo: registro → clases → test → recompensas', async ({ page }) => {
  const u = randomUser();

  await page.goto('http://127.0.0.1:8000/');

  // --- Abrir pestaña "Crear cuenta" ---
  await page.locator('#tab-register').click();

  // Scope al formulario de registro para evitar ambigüedades
  const reg = page.locator('#form-register');
  await expect(reg).toBeVisible();

  await reg.getByLabel('Nombre completo').fill(u.name);
  await reg.getByLabel('Curso').selectOption(u.course);
  await reg.getByLabel('Usuario').fill(u.username);
  await reg.getByLabel('Contraseña').fill(u.password);
  await reg.getByRole('button', { name: 'Crear cuenta' }).click();

  // --- Dashboard visible ---
  await expect(page.getByText('EduSmart Dashboard')).toBeVisible();

  // --- Video Clases ---
  await page.getByRole('link', { name: /Video Clases/i }).click();
  // espera a que cargue la vista de clases (chips o sección de videos)
  await page.waitForSelector('#videos-section, #materias');

const card = page.locator('.video-card').first();
const marcar = card.getByRole('button', { name: 'Marcar como visto' });
if (await marcar.isVisible().catch(() => false)) {
  await Promise.all([
    page.waitForResponse(res =>
      res.url().endsWith('/api/video-completo') && res.request().method() === 'POST'
    ),
    marcar.click(),
  ]);
  const badge  = card.getByText('Completado');
  const doneBtn = card.getByRole('button', { name: 'Ya completado' });
  await Promise.race([
    badge.waitFor({ state: 'visible', timeout: 10_000 }).catch(() => {}),
    doneBtn.waitFor({ state: 'visible', timeout: 10_000 }).catch(() => {}),
  ]);
}

// --- Test adaptativo ---
await page.getByRole('link', { name: /Volver al Dashboard/i }).click();
await page.getByRole('link', { name: /Test Adaptativo/i }).click();
await expect(page.getByText('Test Adaptativo')).toBeVisible();

  // Responder 5 preguntas (elige B)
  for (let i = 0; i < 5; i++) {
    await page.getByRole('button').nth(1).click();
    await page.waitForTimeout(1600); // respeta el delay de tu UI
  }
  await expect(page.getByText('Test Completado')).toBeVisible();

  // --- Recompensas ---
  await page.getByRole('link', { name: 'Ver dashboard' }).click();
  await page.getByRole('link', { name: 'Recompensas' }).click();
  await expect(page.getByText('Puntos Totales')).toBeVisible();
});
