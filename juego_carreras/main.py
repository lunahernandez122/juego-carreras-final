# KEVIN HERNÁNDEZ HENAO & LUNA HERNANDEZ MONTOYA
# Juego de Carreras — POO - Proyecto Final (interfaz gráfica con pygame)

import pygame
import sys
import random
from logica import Carro, Moto, Camion, Carrera, Campeonato, Exportador, OPENPYXL_DISPONIBLE

# ──────────────────────────────────────────────
# CONSTANTES DE PANTALLA Y COLORES
# ──────────────────────────────────────────────
ANCHO_V  = 900
ALTO_V   = 620
FPS      = 60

# Paleta
NEGRO      = (10,  10,  15)
GRIS_OSC   = (28,  28,  38)
GRIS_MED   = (50,  50,  65)
GRIS_CLAR  = (120, 120, 140)
BLANCO     = (240, 240, 250)
AMARILLO   = (255, 210,  50)
NARANJA    = (255, 140,  30)
ROJO       = (220,  50,  50)
VERDE      = (50,  200, 100)
AZUL_CLAR  = (80,  160, 255)
MORADO     = (140,  80, 220)
TURBO_CLR  = (255, 200,   0)

# Colores por tipo de vehículo (para las barras de progreso)
COLOR_VEH = {
    "Carro":  (255, 100,  80),
    "Moto":   ( 80, 160, 255),
    "Camion": ( 80, 200, 100),
}

# ──────────────────────────────────────────────
# HELPERS DE DIBUJO
# ──────────────────────────────────────────────

def dibujar_rect_redondeado(surf, color, rect, radio=8):
    pygame.draw.rect(surf, color, rect, border_radius=radio)

def dibujar_texto(surf, texto, fuente, color, x, y, centrado=False):
    img = fuente.render(texto, True, color)
    rect = img.get_rect()
    if centrado:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)
    surf.blit(img, rect)
    return rect

def dibujar_boton(surf, texto, fuente, rect, color_fondo, color_texto,
                  hover=False, radio=10):
    c = tuple(min(255, v + 30) for v in color_fondo) if hover else color_fondo
    dibujar_rect_redondeado(surf, c, rect, radio)
    dibujar_texto(surf, texto, fuente, color_texto,
                  rect.centerx, rect.centery, centrado=True)

def mouse_sobre(rect):
    return rect.collidepoint(pygame.mouse.get_pos())


# ──────────────────────────────────────────────
# PANTALLA DE INICIO
# ──────────────────────────────────────────────

class PantallaInicio:
    """Solicita nombre del piloto, nombre del vehículo y tipo de vehículo."""

    def __init__(self, pantalla, fuentes):
        self.pantalla  = pantalla
        self.f         = fuentes
        self.nombre_p  = ""
        self.nombre_v  = ""
        self.tipo_sel  = 0           # 0 = sin seleccionar, 1/2/3
        self.campo_act = "piloto"    # "piloto" | "vehiculo"
        self.error     = ""

        # Rectángulos de los botones de tipo
        self.btn_tipos = [
            pygame.Rect(120, 310, 200, 55),
            pygame.Rect(345, 310, 200, 55),
            pygame.Rect(570, 310, 200, 55),
        ]
        self.btn_jugar = pygame.Rect(330, 490, 240, 52)

    def manejar_evento(self, evento):
        if evento.type == pygame.KEYDOWN:
            if self.campo_act == "piloto":
                if evento.key == pygame.K_BACKSPACE:
                    self.nombre_p = self.nombre_p[:-1]
                elif evento.key == pygame.K_TAB:
                    self.campo_act = "vehiculo"
                elif len(self.nombre_p) < 20:
                    self.nombre_p += evento.unicode
            else:
                if evento.key == pygame.K_BACKSPACE:
                    self.nombre_v = self.nombre_v[:-1]
                elif evento.key == pygame.K_TAB:
                    self.campo_act = "piloto"
                elif len(self.nombre_v) < 20:
                    self.nombre_v += evento.unicode

        if evento.type == pygame.MOUSEBUTTONDOWN:
            # Selección de tipo de vehículo
            for i, rect in enumerate(self.btn_tipos, 1):
                if rect.collidepoint(evento.pos):
                    self.tipo_sel = i

            # Clic en campos de texto
            campo_p = pygame.Rect(250, 195, 400, 44)
            campo_v = pygame.Rect(250, 255, 400, 44)
            if campo_p.collidepoint(evento.pos):
                self.campo_act = "piloto"
            if campo_v.collidepoint(evento.pos):
                self.campo_act = "vehiculo"

            # Botón jugar
            if self.btn_jugar.collidepoint(evento.pos):
                return self._validar()
        return None

    def _validar(self):
        np = self.nombre_p.strip() or "Piloto"
        nv = self.nombre_v.strip() or "Mi Vehículo"
        if self.tipo_sel == 0:
            self.error = "⚠ Elige un tipo de vehículo."
            return None
        return (np, nv, self.tipo_sel)

    def dibujar(self):
        s = self.pantalla
        s.fill(NEGRO)

        # Título
        dibujar_texto(s, "🏎  JUEGO DE CARRERAS", self.f["grande"],
                      AMARILLO, ANCHO_V // 2, 60, centrado=True)
        dibujar_texto(s, "Programación Orientada a Objetos — Pascual Bravo",
                      self.f["pequeño"], GRIS_CLAR, ANCHO_V // 2, 95, centrado=True)

        # Campos
        labels = [("Nombre del piloto:", 195), ("Nombre del vehículo:", 255)]
        campos  = [
            (pygame.Rect(250, 195, 400, 44), self.nombre_p, "piloto"),
            (pygame.Rect(250, 255, 400, 44), self.nombre_v, "vehiculo"),
        ]
        for (rect, val, clave), (lbl, _) in zip(campos, labels):
            dibujar_texto(s, lbl, self.f["normal"], GRIS_CLAR, 100, rect.y + 10)
            activo = self.campo_act == clave
            borde = AMARILLO if activo else GRIS_MED
            dibujar_rect_redondeado(s, GRIS_OSC, rect, 8)
            pygame.draw.rect(s, borde, rect, 2, border_radius=8)
            cursor = "|" if activo and (pygame.time.get_ticks() // 500) % 2 == 0 else ""
            dibujar_texto(s, val + cursor, self.f["normal"], BLANCO, rect.x + 10, rect.y + 10)

        # Selector de tipo de vehículo
        dibujar_texto(s, "Tipo de vehículo:", self.f["normal"], GRIS_CLAR, 100, 295)
        tipos = [("🚗  Carro\n+10m/turno", 1), ("🏍  Moto\n+15m/turno", 2), ("🚛  Camión\n+5m/turno", 3)]
        for rect, (etq, tid) in zip(self.btn_tipos, tipos):
            sel = self.tipo_sel == tid
            col = NARANJA if sel else GRIS_OSC
            borde = AMARILLO if sel else GRIS_MED
            dibujar_rect_redondeado(s, col, rect, 10)
            pygame.draw.rect(s, borde, rect, 2, border_radius=10)
            lineas = etq.split("\n")
            dibujar_texto(s, lineas[0], self.f["normal"], BLANCO,
                          rect.centerx, rect.y + 14, centrado=True)
            dibujar_texto(s, lineas[1], self.f["pequeño"], GRIS_CLAR,
                          rect.centerx, rect.y + 34, centrado=True)

        # Botón jugar
        dibujar_boton(s, "▶  COMENZAR CAMPEONATO", self.f["normal"],
                      self.btn_jugar, VERDE, NEGRO,
                      hover=mouse_sobre(self.btn_jugar))

        # Error
        if self.error:
            dibujar_texto(s, self.error, self.f["normal"], ROJO,
                          ANCHO_V // 2, 465, centrado=True)

        # Instrucción TAB
        dibujar_texto(s, "TAB para cambiar campo activo",
                      self.f["pequeño"], GRIS_MED, ANCHO_V // 2, 555, centrado=True)


# ──────────────────────────────────────────────
# PANTALLA DE CARRERA
# ──────────────────────────────────────────────

class PantallaCarrera:
    """Pantalla principal del turno a turno de una carrera."""

    ESTADO_RIVALES   = "rivales"     # procesando turno de rivales
    ESTADO_JUGADOR   = "jugador"     # esperando decisión del jugador
    ESTADO_RESULTADO = "resultado"   # mostrando resultado final de la carrera

    def __init__(self, pantalla, fuentes, carrera: Carrera, num_carrera: int, total: int):
        self.pantalla   = pantalla
        self.f          = fuentes
        self.carrera    = carrera
        self.num        = num_carrera
        self.total      = total
        self.estado     = self.ESTADO_RIVALES
        self.log        = []          # líneas de eventos a mostrar
        self.eventos_pendientes: list[str] = []

        # Botones de acción del jugador
        self.btn_acelerar = pygame.Rect(100, 540, 300, 52)
        self.btn_turbo    = pygame.Rect(500, 540, 300, 52)
        self.btn_sig      = pygame.Rect(330, 520, 240, 52)

        # Animación de progreso
        self._ejecutar_rivales()

    def _ejecutar_rivales(self):
        eventos = self.carrera.ejecutar_turno_rivales()
        for e in eventos:
            for linea in e.split("\n"):
                if linea.strip():
                    self.log.append(linea.strip())
        self.log = self.log[-8:]   # máximo 8 líneas visibles
        self.estado = self.ESTADO_JUGADOR

    def manejar_evento(self, evento):
        if evento.type != pygame.MOUSEBUTTONDOWN:
            return None

        if self.estado == self.ESTADO_JUGADOR:
            jugador = self._jugador()
            if jugador and jugador.posicion < self.carrera.distancia:
                if self.btn_acelerar.collidepoint(evento.pos):
                    self._accion_jugador(False)
                elif self.btn_turbo.collidepoint(evento.pos):
                    self._accion_jugador(True)
            # Si el jugador ya llegó, pasar directo a resultado
            if jugador and jugador.posicion >= self.carrera.distancia:
                self.estado = self.ESTADO_RESULTADO

        elif self.estado == self.ESTADO_RESULTADO:
            if self.btn_sig.collidepoint(evento.pos):
                return "siguiente"
        return None

    def _accion_jugador(self, usar_turbo: bool):
        eventos = self.carrera.ejecutar_accion_jugador(usar_turbo)
        for e in eventos:
            for linea in e.split("\n"):
                if linea.strip():
                    self.log.append(linea.strip())
        self.log = self.log[-8:]

        # Verificar si alguien llegó a la meta
        if self.carrera.verificar_ganador():
            self.estado = self.ESTADO_RESULTADO
        else:
            # Turno de rivales
            self._ejecutar_rivales()

    def _jugador(self):
        for v in self.carrera.vehiculos:
            if v.es_jugador:
                return v
        return None

    def dibujar(self):
        s = self.pantalla
        s.fill(NEGRO)

        # Cabecera
        titulo = f"CARRERA {self.num}/{self.total}  |  Meta: {self.carrera.distancia}m  |  {self.carrera.dificultad_nombre}  |  Turno {self.carrera.turno_actual}"
        dibujar_texto(s, titulo, self.f["normal"], AMARILLO, ANCHO_V // 2, 18, centrado=True)

        # ── Barras de progreso ──
        y_barra = 55
        jugador = self._jugador()
        ranking = self.carrera.ranking()

        for pos, v in enumerate(ranking, 1):
            es_j = v.es_jugador
            nombre_disp = f"{'★ ' if es_j else ''}{v.nombre[:14]}"
            color = AMARILLO if es_j else COLOR_VEH.get(type(v).__name__, GRIS_CLAR)

            # Etiqueta posición
            medallas = {1: "1°", 2: "2°", 3: "3°"}
            pos_txt = medallas.get(pos, f"{pos}°")
            dibujar_texto(s, pos_txt, self.f["pequeño"], GRIS_CLAR, 10, y_barra + 5)
            dibujar_texto(s, nombre_disp, self.f["pequeño"], color, 40, y_barra + 5)

            # Barra de fondo
            barra_x, barra_w = 220, 540
            bg_rect = pygame.Rect(barra_x, y_barra, barra_w, 22)
            dibujar_rect_redondeado(s, GRIS_OSC, bg_rect, 5)

            # Barra de progreso
            prog = min(v.posicion / self.carrera.distancia, 1.0)
            fill_w = max(4, int(barra_w * prog))
            fill_rect = pygame.Rect(barra_x, y_barra, fill_w, 22)
            bar_col = tuple(max(0, c - 60) for c in color) if not es_j else (200, 160, 0)
            dibujar_rect_redondeado(s, bar_col, fill_rect, 5)

            # Posición en metros + turbos
            dibujar_texto(s, f"{v.posicion}m", self.f["pequeño"], BLANCO, barra_x + barra_w + 8, y_barra + 5)
            dibujar_texto(s, f"T:{v.turbos}", self.f["pequeño"], TURBO_CLR, barra_x + barra_w + 60, y_barra + 5)

            y_barra += 30

        # ── Log de eventos ──
        sep_y = y_barra + 8
        pygame.draw.line(s, GRIS_MED, (10, sep_y), (ANCHO_V - 10, sep_y))
        log_y = sep_y + 8
        for linea in self.log[-8:]:
            dibujar_texto(s, linea, self.f["pequeño"], GRIS_CLAR, 20, log_y)
            log_y += 18

        # ── Área de acciones ──
        if self.estado == self.ESTADO_JUGADOR and jugador:
            if jugador.posicion < self.carrera.distancia:
                pygame.draw.line(s, GRIS_MED, (10, 530), (ANCHO_V - 10, 530))
                # Info jugador
                tipo_j = type(jugador).__name__
                avance = 10 if tipo_j == "Carro" else 15 if tipo_j == "Moto" else 5
                dibujar_texto(s, f"Tu turno — {jugador.nombre}  |  Pos: {jugador.posicion}m  |  Turbos: {jugador.turbos}",
                              self.f["pequeño"], AMARILLO, ANCHO_V // 2, 516, centrado=True)

                # Botón acelerar
                dibujar_boton(s, f"🚗 Acelerar (+{avance}m)", self.f["normal"],
                              self.btn_acelerar, AZUL_CLAR, NEGRO,
                              hover=mouse_sobre(self.btn_acelerar))

                # Botón turbo (deshabilitado si no hay turbos)
                t_col = NARANJA if jugador.turbos > 0 else GRIS_MED
                dibujar_boton(s, f"🚀 Turbo [{jugador.turbos}] (+{avance}m+extra)", self.f["normal"],
                              self.btn_turbo, t_col, NEGRO,
                              hover=mouse_sobre(self.btn_turbo) and jugador.turbos > 0)
            else:
                # Jugador ya llegó, esperar a que todo termine
                dibujar_texto(s, "¡Llegaste a la meta! Esperando rivales...",
                              self.f["normal"], VERDE, ANCHO_V // 2, 550, centrado=True)
                self.estado = self.ESTADO_RESULTADO

        elif self.estado == self.ESTADO_RESULTADO:
            self._dibujar_resultado()

    def _dibujar_resultado(self):
        s = self.pantalla
        # Panel semitransparente
        overlay = pygame.Surface((ANCHO_V, 220), pygame.SRCALPHA)
        overlay.fill((10, 10, 20, 220))
        s.blit(overlay, (0, 390))

        pygame.draw.line(s, AMARILLO, (10, 392), (ANCHO_V - 10, 392), 2)

        ranking = self.carrera.ranking()
        ganador = ranking[0]
        jugador = self._jugador()
        pos_j   = ranking.index(jugador) + 1 if jugador else 0
        puntos  = self.carrera.puntos_jugador()

        medallas_txt = {1: "🥇 1°", 2: "🥈 2°", 3: "🥉 3°"}
        dibujar_texto(s, f"FIN — Ganador: {ganador.nombre}", self.f["grande"],
                      AMARILLO, ANCHO_V // 2, 412, centrado=True)

        if jugador:
            pos_str = medallas_txt.get(pos_j, f"{pos_j}°")
            msg = f"Terminaste {pos_str}  |  +{puntos} pts"
            col = VERDE if pos_j == 1 else AZUL_CLAR if pos_j <= 3 else BLANCO
            dibujar_texto(s, msg, self.f["normal"], col,
                          ANCHO_V // 2, 450, centrado=True)

        # Podio rápido
        podio_y = 480
        for i, v in enumerate(ranking[:3], 1):
            med = ["🥇", "🥈", "🥉"][i - 1]
            dibujar_texto(s, f"{med} {v.nombre} — {v.posicion}m",
                          self.f["pequeño"], BLANCO,
                          ANCHO_V // 2, podio_y, centrado=True)
            podio_y += 18

        # Botón siguiente
        lbl = "▶ Siguiente carrera" if self.num < self.total else "🏁 Ver resultados finales"
        dibujar_boton(s, lbl, self.f["normal"], self.btn_sig, VERDE, NEGRO,
                      hover=mouse_sobre(self.btn_sig))


# ──────────────────────────────────────────────
# PANTALLA DE PREPARACIÓN DE CARRERA
# ──────────────────────────────────────────────

class PantallaPreparacion:
    """Muestra info de la carrera (distancia, dificultad, rivales) antes de empezar."""

    def __init__(self, pantalla, fuentes, carrera: Carrera, num: int, total: int):
        self.pantalla = pantalla
        self.f        = fuentes
        self.carrera  = carrera
        self.num      = num
        self.total    = total
        self.btn_ok   = pygame.Rect(330, 520, 240, 52)

    def manejar_evento(self, evento):
        if evento.type == pygame.MOUSEBUTTONDOWN:
            if self.btn_ok.collidepoint(evento.pos):
                return "iniciar"
        return None

    def dibujar(self):
        s = self.pantalla
        s.fill(NEGRO)

        dibujar_texto(s, f"CARRERA {self.num} DE {self.total}", self.f["grande"],
                      AMARILLO, ANCHO_V // 2, 50, centrado=True)
        dibujar_texto(s, f"Distancia: {self.carrera.distancia}m  |  Dificultad: {self.carrera.dificultad_nombre}",
                      self.f["normal"], BLANCO, ANCHO_V // 2, 105, centrado=True)

        turbos_j = self.carrera.cfg["turbos_jugador"]
        prob_riv = int(self.carrera.cfg["prob_turbo_rival"] * 100)
        prob_obs = int(self.carrera.cfg["prob_obstaculo"] * 100)
        dibujar_texto(s, f"Turbos iniciales: {turbos_j}  |  Prob. turbo rival: {prob_riv}%  |  Prob. obstáculo: {prob_obs}%",
                      self.f["pequeño"], GRIS_CLAR, ANCHO_V // 2, 140, centrado=True)

        dibujar_texto(s, "RIVALES", self.f["normal"], NARANJA, ANCHO_V // 2, 185, centrado=True)
        y = 215
        for v in self.carrera.vehiculos:
            if not v.es_jugador:
                icono = "🚗" if type(v).__name__ == "Carro" else "🏍" if type(v).__name__ == "Moto" else "🚛"
                dibujar_texto(s, f"  {icono}  {v.nombre}  ({type(v).__name__})",
                              self.f["pequeño"], BLANCO, ANCHO_V // 2, y, centrado=True)
                y += 26

        dibujar_boton(s, "▶  ¡ARRANCAR!", self.f["normal"],
                      self.btn_ok, VERDE, NEGRO,
                      hover=mouse_sobre(self.btn_ok))


# ──────────────────────────────────────────────
# PANTALLA DE FIN DE CAMPEONATO
# ──────────────────────────────────────────────

class PantallaFinal:
    """Muestra clasificación acumulada y permite exportar resultados."""

    def __init__(self, pantalla, fuentes, campeonato: Campeonato):
        self.pantalla    = pantalla
        self.f           = fuentes
        self.campeonato  = campeonato
        self.exportador  = Exportador(campeonato)
        self.msg_export  = ""

        self.btn_csv  = pygame.Rect(60,  545, 140, 45)
        self.btn_json = pygame.Rect(220, 545, 140, 45)
        self.btn_txt  = pygame.Rect(380, 545, 140, 45)
        self.btn_xlsx = pygame.Rect(540, 545, 140, 45)
        self.btn_exit = pygame.Rect(730, 545, 120, 45)

    def manejar_evento(self, evento):
        if evento.type != pygame.MOUSEBUTTONDOWN:
            return None
        for btn, fmt in [
            (self.btn_csv, "csv"),
            (self.btn_json, "json"),
            (self.btn_txt, "txt"),
        ]:
            if btn.collidepoint(evento.pos):
                try:
                    arch = self.exportador.exportar(fmt)
                    self.msg_export = f"✅ Exportado: {arch}"
                except Exception as e:
                    self.msg_export = f"❌ Error: {e}"

        if self.btn_xlsx.collidepoint(evento.pos):
            if OPENPYXL_DISPONIBLE:
                try:
                    arch = self.exportador.exportar("xlsx")
                    self.msg_export = f"✅ Exportado: {arch}"
                except Exception as e:
                    self.msg_export = f"❌ Error: {e}"
            else:
                self.msg_export = "⚠ Instala openpyxl: pip install openpyxl"

        if self.btn_exit.collidepoint(evento.pos):
            return "salir"
        return None

    def dibujar(self):
        s = self.pantalla
        s.fill(NEGRO)

        dibujar_texto(s, "🏁  FIN DEL CAMPEONATO", self.f["grande"],
                      AMARILLO, ANCHO_V // 2, 25, centrado=True)
        dibujar_texto(s, f"Piloto: {self.campeonato.nombre_jugador}  |  Puntaje total: {self.campeonato.puntaje_total} pts",
                      self.f["normal"], BLANCO, ANCHO_V // 2, 65, centrado=True)

        # Resumen de carreras
        y = 105
        dibujar_texto(s, "Resumen de carreras:", self.f["normal"], NARANJA, 40, y)
        y += 28
        for r in self.campeonato.resultados:
            pts_str = f"+{r['puntos']}" if r['puntos'] > 0 else str(r['puntos'])
            txt = (f"  Carrera {r['carrera']}: {r['distancia']}m — "
                   f"{r['dificultad']} — {r['turnos']} turnos → {pts_str} pts")
            dibujar_texto(s, txt, self.f["pequeño"], BLANCO, 40, y)
            y += 22

        # Clasificación acumulada
        y += 12
        pygame.draw.line(s, GRIS_MED, (10, y), (ANCHO_V - 10, y))
        y += 8
        dibujar_texto(s, "CLASIFICACIÓN ACUMULADA FINAL", self.f["normal"], NARANJA,
                      ANCHO_V // 2, y, centrado=True)
        y += 28

        # Encabezados de tabla
        cols = [(35, "Pos"), (90, "Nombre"), (260, "Tipo"), (380, "Dist.total"),
                (510, "Pts F1"), (630, "Turbos")]
        for cx, lbl in cols:
            dibujar_texto(s, lbl, self.f["pequeño"], GRIS_CLAR, cx, y)
        y += 22
        pygame.draw.line(s, GRIS_MED, (10, y), (ANCHO_V - 10, y))
        y += 6

        medallas = {1: "🥇", 2: "🥈", 3: "🥉"}
        tabla = self.campeonato.clasificacion_acumulada()
        for pos, fila in enumerate(tabla, 1):
            med = medallas.get(pos, f"{pos}°")
            color = AMARILLO if fila["Nombre"] == self.campeonato.nombre_vehiculo else BLANCO
            datos = [
                (35, med),
                (90, fila["Nombre"][:16]),
                (260, fila["Tipo"]),
                (380, f"{fila['Distancia total (m)']}m"),
                (510, str(fila["Puntos totales"])),
                (630, str(fila["Turbos totales usados"])),
            ]
            for cx, txt in datos:
                dibujar_texto(s, txt, self.f["pequeño"], color, cx, y)
            y += 20
            if y > 510:
                break

        # Botones de exportación
        for btn, lbl, col in [
            (self.btn_csv, "CSV", AZUL_CLAR),
            (self.btn_json, "JSON", MORADO),
            (self.btn_txt, "TXT", VERDE),
            (self.btn_xlsx, "XLSX", NARANJA if OPENPYXL_DISPONIBLE else GRIS_MED),
        ]:
            dibujar_boton(s, lbl, self.f["normal"], btn, col, NEGRO,
                          hover=mouse_sobre(btn))

        dibujar_boton(s, "Salir", self.f["normal"], self.btn_exit, ROJO, BLANCO,
                      hover=mouse_sobre(self.btn_exit))

        # Mensaje de exportación
        if self.msg_export:
            dibujar_texto(s, self.msg_export, self.f["pequeño"],
                          VERDE if self.msg_export.startswith("✅") else ROJO,
                          ANCHO_V // 2, 600, centrado=True)


# ──────────────────────────────────────────────
# CONTROLADOR PRINCIPAL
# ──────────────────────────────────────────────

def main():
    pygame.init()
    pantalla = pygame.display.set_mode((ANCHO_V, ALTO_V))
    pygame.display.set_caption("🏎 Juego de Carreras — POO")
    reloj = pygame.time.Clock()

    # Fuentes
    try:
        f_grande  = pygame.font.SysFont("segoeuiemoji", 28, bold=True)
        f_normal  = pygame.font.SysFont("segoeuiemoji", 18)
        f_pequeño = pygame.font.SysFont("segoeuiemoji", 14)
    except Exception:
        f_grande  = pygame.font.SysFont(None, 30, bold=True)
        f_normal  = pygame.font.SysFont(None, 20)
        f_pequeño = pygame.font.SysFont(None, 16)

    fuentes = {"grande": f_grande, "normal": f_normal, "pequeño": f_pequeño}

    # ── Estado del juego ──
    FASE_INICIO      = "inicio"
    FASE_PREP        = "preparacion"
    FASE_CARRERA     = "carrera"
    FASE_FINAL       = "final"

    fase       = FASE_INICIO
    campeonato = None
    carrera_actual = None
    num_carrera    = 0
    pantalla_obj   = PantallaInicio(pantalla, fuentes)

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            resultado = pantalla_obj.manejar_evento(evento)

            # ── Transiciones de estado ──
            if fase == FASE_INICIO and resultado:
                nombre_p, nombre_v, tipo = resultado
                campeonato = Campeonato.nuevo(nombre_p, nombre_v, tipo)
                num_carrera = 0
                fase = FASE_PREP
                num_carrera += 1
                carrera_actual = Carrera.crear_aleatoria()
                carrera_actual.registrar_vehiculo(campeonato.nombre_vehiculo, campeonato.tipo_vehiculo)
                carrera_actual.agregar_rivales_aleatorios()
                carrera_actual.asignar_dificultad_aleatoria()
                pantalla_obj = PantallaPreparacion(pantalla, fuentes, carrera_actual,
                                                   num_carrera, Campeonato.TOTAL_CARRERAS)

            elif fase == FASE_PREP and resultado == "iniciar":
                fase = FASE_CARRERA
                pantalla_obj = PantallaCarrera(pantalla, fuentes, carrera_actual,
                                               num_carrera, Campeonato.TOTAL_CARRERAS)

            elif fase == FASE_CARRERA and resultado == "siguiente":
                campeonato.registrar_resultado(carrera_actual)
                if num_carrera < Campeonato.TOTAL_CARRERAS:
                    num_carrera += 1
                    carrera_actual = Carrera.crear_aleatoria()
                    carrera_actual.registrar_vehiculo(campeonato.nombre_vehiculo, campeonato.tipo_vehiculo)
                    carrera_actual.agregar_rivales_aleatorios()
                    carrera_actual.asignar_dificultad_aleatoria()
                    fase = FASE_PREP
                    pantalla_obj = PantallaPreparacion(pantalla, fuentes, carrera_actual,
                                                       num_carrera, Campeonato.TOTAL_CARRERAS)
                else:
                    fase = FASE_FINAL
                    pantalla_obj = PantallaFinal(pantalla, fuentes, campeonato)

            elif fase == FASE_FINAL and resultado == "salir":
                pygame.quit()
                sys.exit()

        pantalla_obj.dibujar()
        pygame.display.flip()
        reloj.tick(FPS)


if __name__ == "__main__":
    main()
