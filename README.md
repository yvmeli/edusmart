<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1"/>
  <title>EduSmart - Práctica</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
  <style>
    /* Variables CSS */
    :root {
      --primary-500: #3b82f6;
      --primary-600: #2563eb;
      --primary-700: #1d4ed8;
      --success-500: #10b981;
      --warning-500: #f59e0b;
      --error-500: #ef4444;
      --info-500: #06b6d4;
      --secondary-50: #f8fafc;
      --secondary-100: #f1f5f9;
      --secondary-200: #e2e8f0;
      --secondary-400: #94a3b8;
      --secondary-500: #64748b;
      --secondary-600: #475569;
      --secondary-700: #334155;
      --secondary-800: #1e293b;
      --secondary-900: #0f172a;
      --surface: #ffffff;
      --background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      --shadow-sm: 0 1px 3px 0 rgb(0 0 0 / 0.1);
      --shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.1);
      --shadow-lg: 0 10px 15px -3px rgb(0 0 0 / 0.1);
      --shadow-xl: 0 20px 25px -5px rgb(0 0 0 / 0.1);
      --radius-lg: 12px;
      --radius-xl: 16px;
      --transition-fast: 150ms ease;
      --transition-normal: 250ms ease;
    }

    * { box-sizing: border-box; margin: 0; padding: 0; }

    body {
      font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      background: var(--background);
      color: var(--secondary-900);
      line-height: 1.6;
      min-height: 100vh;
    }

    .container {
      max-width: 1200px;
      margin: 0 auto;
      padding: 24px;
      min-height: 100vh;
    }

    .header {
      background: linear-gradient(135deg, rgba(59, 130, 246, 0.95), rgba(29, 78, 216, 0.95));
      backdrop-filter: blur(10px);
      border-radius: var(--radius-xl);
      padding: 32px;
      margin-bottom: 32px;
      box-shadow: var(--shadow-lg);
      border: 1px solid rgba(255, 255, 255, 0.2);
      display: flex;
      justify-content: space-between;
      align-items: center;
    }

    .header h1 {
      font-size: 2.5rem;
      font-weight: 700;
      color: white;
      text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
    }

    .header p {
      color: rgba(255, 255, 255, 0.9);
      font-size: 1.125rem;
      text-shadow: 0 1px 2px rgba(0, 0, 0, 0.2);
      margin-top: 8px;
    }

    .nav-buttons {
      display: flex;
      gap: 12px;
    }

    /* Practice Modes */
    .practice-modes {
      background: var(--surface);
      border-radius: var(--radius-xl);
      padding: 32px;
      box-shadow: var(--shadow-lg);
      border: 1px solid var(--secondary-200);
      margin-bottom: 24px;
    }

    .modes-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
      gap: 20px;
      margin-top: 24px;
    }

    .practice-card {
      background: var(--surface);
      border: 2px solid var(--secondary-200);
      border-radius: var(--radius-xl);
      padding: 24px;
      cursor: pointer;
      transition: all var(--transition-normal);
      text-align: center;
      position: relative;
      overflow: hidden;
    }

    .practice-card::before {
      content: '';
      position: absolute;
      top: 0;
      left: -100%;
      width: 100%;
      height: 100%;
      background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
      transition: left 0.5s;
    }

    .practice-card:hover::before {
      left: 100%;
    }

    .practice-card:hover {
      border-color: var(--primary-500);
      transform: translateY(-4px);
      box-shadow: var(--shadow-xl);
    }

    .practice-icon {
      width: 64px;
      height: 64px;
      margin: 0 auto 16px;
      border-radius: var(--radius-lg);
      display: flex;
      align-items: center;
      justify-content: center;
      color: white;
    }

    .practice-icon.flashcards { background: linear-gradient(135deg, var(--primary-500), var(--primary-700)); }
    .practice-icon.quiz { background: linear-gradient(135deg, var(--success-500), #059669); }
    .practice-icon.challenge { background: linear-gradient(135deg, var(--warning-500), #d97706); }
    .practice-icon.review { background: linear-gradient(135deg, var(--info-500), #0284c7); }

    .practice-card h3 {
      font-size: 1.25rem;
      font-weight: 600;
      margin-bottom: 12px;
      color: var(--secondary-900);
    }

    .practice-card p {
      color: var(--secondary-600);
      margin-bottom: 16px;
      line-height: 1.5;
    }

    /* Progress Section */
    .progress-section {
      display: grid;
      grid-template-columns: 2fr 1fr;
      gap: 24px;
      margin-bottom: 24px;
    }

    .progress-card {
      background: var(--surface);
      border-radius: var(--radius-xl);
      padding: 32px;
      box-shadow: var(--shadow-lg);
      border: 1px solid var(--secondary-200);
    }

    .subject-progress {
      display: flex;
      flex-direction: column;
      gap: 20px;
    }

    .subject-item {
      display: flex;
      align-items: center;
      gap: 16px;
      padding: 16px;
      background: var(--secondary-50);
      border-radius: var(--radius-lg);
    }

    .subject-icon {
      width: 48px;
      height: 48px;
      border-radius: var(--radius-lg);
      display: flex;
      align-items: center;
      justify-content: center;
      color: white;
      flex-shrink: 0;
    }

    .subject-icon.math { background: linear-gradient(135deg, #8b5cf6, #7c3aed); }
    .subject-icon.language { background: linear-gradient(135deg, #06b6d4, #0891b2); }
    .subject-icon.science { background: linear-gradient(135deg, #10b981, #059669); }

    .subject-info {
      flex: 1;
    }

    .subject-name {
      font-weight: 600;
      color: var(--secondary-900);
      margin-bottom: 4px;
    }

    .subject-stats {
      font-size: 0.875rem;
      color: var(--secondary-600);
      margin-bottom: 8px;
    }

    .progress-bar {
      width: 100%;
      height: 6px;
      background: var(--secondary-200);
      border-radius: 3px;
      overflow: hidden;
    }

    .progress-fill {
      height: 100%;
      background: var(--primary-500);
      transition: width 1s ease;
    }

    /* Quick Stats */
    .quick-stats {
      display: grid;
      grid-template-rows: repeat(3, 1fr);
      gap: 16px;
    }

    .stat-item {
      background: var(--secondary-50);
      padding: 20px;
      border-radius: var(--radius-lg);
      text-align: center;
    }

    .stat-value {
      font-size: 2rem;
      font-weight: 700;
      color: var(--primary-600);
      margin-bottom: 4px;
    }

    .stat-label {
      font-size: 0.875rem;
      color: var(--secondary-600);
    }

    /* Buttons */
    .btn {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      padding: 12px 20px;
      border: none;
      border-radius: var(--radius-lg);
      font-weight: 600;
      cursor: pointer;
      transition: all var(--transition-fast);
      text-decoration: none;
      font-size: 0.875rem;
    }

    .btn-primary {
      background: linear-gradient(135deg, var(--primary-500), var(--primary-700));
      color: white;
    }

    .btn-primary:hover {
      transform: translateY(-2px);
      box-shadow: var(--shadow-lg);
    }

    .btn-secondary {
      background: rgba(255, 255, 255, 0.2);
      color: white;
      border: 1px solid rgba(255, 255, 255, 0.3);
    }

    .btn-secondary:hover {
      background: rgba(255, 255, 255, 0.3);
    }

    .badge {
      display: inline-block;
      padding: 4px 12px;
      border-radius: var(--radius-lg);
      font-size: 0.75rem;
      font-weight: 600;
    }

    .badge-primary { background: rgba(59, 130, 246, 0.1); color: var(--primary-700); }
    .badge-success { background: rgba(16, 185, 129, 0.1); color: var(--success-500); }
    .badge-warning { background: rgba(245, 158, 11, 0.1); color: var(--warning-500); }
    .badge-info { background: rgba(6, 182, 212, 0.1); color: var(--info-500); }

    /* Responsive */
    @media (max-width: 768px) {
      .container { padding: 16px; }
      .progress-section { grid-template-columns: 1fr; }
      .modes-grid { grid-template-columns: 1fr; }
      .header { flex-direction: column; text-align: center; gap: 16px; }
    }

    /* Animations */
    @keyframes fadeInUp {
      from { opacity: 0; transform: translateY(20px); }
      to { opacity: 1; transform: translateY(0); }
    }

    .animate-fade-in {
      animation: fadeInUp 0.6s ease forwards;
    }

    .section-title {
      font-size: 1.5rem;
      font-weight: 600;
      color: var(--secondary-900);
      margin-bottom: 8px;
    }

    .section-subtitle {
      color: var(--secondary-600);
      margin-bottom: 24px;
    }
  </style>
</head>
<body>
  <div class="container">
    <!-- Header -->
    <div class="header animate-fade-in">
      <div>
        <h1>Práctica Interactiva</h1>
        <p>Refuerza tus conocimientos con ejercicios personalizados</p>
      </div>
      <div class="nav-buttons">
        <a href="menu.html" class="btn btn-secondary">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="m3 9 9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/>
          </svg>
          Dashboard
        </a>
        <a href="test.html" class="btn btn-secondary">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M9 11H5a2 2 0 0 0-2 2v3c0 1.1.9 2 2 2h2"/>
            <path d="M11 13.6V21H8"/>
            <path d="M16 21h-2c0-4.4 3.6-8 8-8"/>
            <circle cx="20" cy="8" r="2"/>
          </svg>
          Evaluaciones
        </a>
      </div>
    </div>

    <!-- Progress Overview -->
    <div class="progress-section animate-fade-in">
      <div class="progress-card">
        <h2 class="section-title">Progreso por Materia</h2>
        <p class="section-subtitle">Tu avance en cada área de conocimiento</p>
        
        <div class="subject-progress">
          <div class="subject-item">
            <div class="subject-icon math">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <rect x="3" y="3" width="18" height="18" rx="2" ry="2"/>
                <path d="M9 9h6v6h-6z"/>
              </svg>
            </div>
            <div class="subject-info">
              <div class="subject-name">Matemáticas</div>
              <div class="subject-stats">24 ejercicios completados • 85% de precisión</div>
              <div class="progress-bar">
                <div class="progress-fill" style="width: 75%;"></div>
              </div>
            </div>
          </div>

          <div class="subject-item">
            <div class="subject-icon language">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                <polyline points="14,2 14,8 20,8"/>
              </svg>
            </div>
            <div class="subject-info">
              <div class="subject-name">Lengua</div>
              <div class="subject-stats">18 ejercicios completados • 92% de precisión</div>
              <div class="progress-bar">
                <div class="progress-fill" style="width: 60%;"></div>
              </div>
            </div>
          </div>

          <div class="subject-item">
            <div class="subject-icon science">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="12" cy="12" r="3"/>
                <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1 1.51V3a2 2 0 0 1 2 2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"/>
              </svg>
            </div>
            <div class="subject-info">
              <div class="subject-name">Ciencias</div>
              <div class="subject-stats">12 ejercicios completados • 78% de precisión</div>
              <div class="progress-bar">
                <div class="progress-fill" style="width: 40%;"></div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="progress-card">
        <h2 class="section-title">Estadísticas Rápidas</h2>
        <div class="quick-stats">
          <div class="stat-item">
            <div class="stat-value">54</div>
            <div class="stat-label">Ejercicios completados</div>
          </div>
          <div class="stat-item">
            <div class="stat-value">85%</div>
            <div class="stat-label">Precisión promedio</div>
          </div>
          <div class="stat-item">
            <div class="stat-value">7</div>
            <div class="stat-label">Días consecutivos</div>
          </div>
        </div>
      </div>
    </div>

    <!-- Practice Modes -->
    <div class="practice-modes animate-fade-in">
      <h2 class="section-title">Modos de Práctica</h2>
      <p class="section-subtitle">Elige el tipo de práctica que prefieras</p>
      
      <div class="modes-grid">
        <div class="practice-card" onclick="startPractice('flashcards')">
          <div class="practice-icon flashcards">
            <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <rect x="3" y="3" width="18" height="18" rx="2" ry="2"/>
              <path d="M9 9h6v6h-6z"/>
            </svg>
          </div>
          <h3>Tarjetas de Memoria</h3>
          <p>Repasa conceptos clave con tarjetas interactivas que se adaptan a tu ritmo de aprendizaje.</p>
          <span class="badge badge-primary">Recomendado</span>
        </div>

        <div class="practice-card" onclick="startPractice('quiz')">
          <div class="practice-icon quiz">
            <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <circle cx="12" cy="12" r="10"/>
              <path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"/>
              <line x1="12" y1="17" x2="12.01" y2="17"/>
            </svg>
          </div>
          <h3>Quiz Rápido</h3>
          <p>Preguntas cortas y dinámicas para practicar en cualquier momento del día.</p>
          <span class="badge badge-success">5-10 min</span>
        </div>

        <div class="practice-card" onclick="startPractice('challenge')">
          <div class="practice-icon challenge">
            <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M6 9H4.5a2.5 2.5 0 0 1 0-5H6"/>
              <path d="M18 9h1.5a2.5 2.5 0 0 0 0-5H18"/>
              <path d="M4 22h16"/>
              <path d="M10 14.66V17c0 .55-.47.98-.97 1.21C7.85 18.75 7 20.24 7 22"/>
              <path d="M14 14.66V17c0 .55.47.98.97 1.21C16.15 18.75 17 20.24 17 22"/>
              <path d="M18 2H6v7a6 6 0 0 0 12 0V2Z"/>
            </svg>
          </div>
          <h3>Desafío Diario</h3>
          <p>Retos especiales que cambian cada día para mantener tu mente activa.</p>
          <span class="badge badge-warning">Nuevo</span>
        </div>

        <div class="practice-card" onclick="startPractice('review')">
          <div class="practice-icon review">
            <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M3 3v5h5"/>
              <path d="M3.05 13A9 9 0 1 0 6 5.3L3 8"/>
              <path d="M12 7v5l4 2"/>
            </svg>
          </div>
          <h3>Repaso Inteligente</h3>
          <p>Revisión automática de temas que necesitas reforzar basada en tu historial.</p>
          <span class="badge badge-info">IA Personalizada</span>
        </div>
      </div>
    </div>
  </div>

  <script>
    function startPractice(mode) {
      const modes = {
        flashcards: 'Tarjetas de Memoria',
        quiz: 'Quiz Rápido', 
        challenge: 'Desafío Diario',
        review: 'Repaso Inteligente'
      };

      showNotification(`Iniciando ${modes[mode]}...`, 'info');
      
      setTimeout(() => {
        // Simular inicio de práctica
        if (mode === 'quiz') {
          window.location.href = 'test.html';
        } else {
          alert(`🎯 ${modes[mode]}\n\n¡Próximamente disponible!\n\nPor ahora puedes usar las evaluaciones para practicar.`);
        }
      }, 1000);
    }

    function showNotification(message, type = 'info') {
      const notification = document.createElement('div');
      notification.style.cssText = `
        position: fixed;
        top: 24px;
        right: 24px;
        background: white;
        border-radius: 12px;
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
        padding: 16px 20px;
        max-width: 400px;
        z-index: 1001;
        transform: translateX(450px);
        transition: transform 0.3s ease;
        border-left: 4px solid ${type === 'success' ? '#10b981' : type === 'error' ? '#ef4444' : '#3b82f6'};
      `;
      
      notification.innerHTML = `
        <div style="display: flex; align-items: center; gap: 12px;">
          <div style="flex: 1;">
            <div style="font-weight: 600; color: #1f2937; margin-bottom: 4px;">
              ${type === 'success' ? 'Éxito' : type === 'error' ? 'Error' : 'Información'}
            </div>
            <div style="font-size: 0.875rem; color: #6b7280;">${message}</div>
          </div>
          <button onclick="this.parentElement.parentElement.remove()" style="background: none; border: none; cursor: pointer; color: #9ca3af; padding: 4px;">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <line x1="18" y1="6" x2="6" y2="18"/>
              <line x1="6" y1="6" x2="18" y2="18"/>
            </svg>
          </button>
        </div>
      `;
      
      document.body.appendChild(notification);
      
      setTimeout(() => {
        notification.style.transform = 'translateX(0)';
      }, 100);
      
      setTimeout(() => {
        notification.style.transform = 'translateX(450px)';
        setTimeout(() => {
          if (notification.parentElement) {
            notification.parentElement.removeChild(notification);
          }
        }, 300);
      }, 4000);
    }

    // Inicialización
    document.addEventListener('DOMContentLoaded', function() {
      console.log('Página de práctica cargada');
    });
  </script>
</body>
</html>