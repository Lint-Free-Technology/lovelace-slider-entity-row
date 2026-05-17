import { LitElement, html, css } from "lit";
import { property } from "lit/decorators.js";
import { query } from "lit/decorators/query.js";

import { getController } from "./controllers/get-controller";
import { Controller, ControllerConfig } from "./controllers/controller";
import pjson from "../package.json";

import "./editor";

class SliderEntityRow extends LitElement {
  _config: ControllerConfig;
  ctrl: Controller;

  @property() hass: any;
  @property({ type: Boolean }) hide_state: boolean;
  @query("ha-slider") _slider?;

  setConfig(config: ControllerConfig) {
    if (config.attribute === "color_temp_mired")
      throw Error("color_temp_mired has been removed");

    this._config = {
      tooltip_distance: 20,
      grow: true,
      ...config,
    };
    if (!config.entity) throw new Error(`No entity specified.`);
    const domain = config.entity.split(".")[0];
    const ctrlClass = getController(domain);
    if (!ctrlClass) throw new Error(`Unsupported entity type: ${domain}`);
    this.ctrl = new ctrlClass(this._config, this);
  }

  static getConfigElement() {
    console.log("GetConfigElement");
    return document.createElement("slider-entity-row-editor");
  }

  async resized() {
    await this.updateComplete;
    if (!this.shadowRoot || !this.parentElement) return;
    this.hide_state = this._config.full_row
      ? this.parentElement?.clientWidth <= 180
      : this.parentElement?.clientWidth <= 335;
    return;
  }

  async firstUpdated() {
    await this.resized();
  }

  async updated() {
    if (!this._slider) return;
    await this._slider.updateComplete;
    if (this._slider.shadowRoot.querySelector("style.slider-entity-row"))
      return;
    const styleEl = document.createElement("style");
    styleEl.classList.add("slider-entity-row");
    styleEl.innerHTML = `span#thumb{box-shadow: var(--slider-entity-row-thumb-box-shadow, inherit);}`;
    this._slider.shadowRoot?.appendChild(styleEl);
    const tooltip = this._slider.shadowRoot?.querySelector("wa-tooltip");
    if (tooltip) {
      tooltip.setAttribute("distance", this._config.tooltip_distance);
    }
  }

  async connectedCallback() {
    super.connectedCallback();
    await this.resized();
  }

  render() {
    const c = this.ctrl;
    c.hass = this.hass;
    if (!c.stateObj)
      return html`
        <hui-warning>
          ${this.hass.localize(
            "ui.panel.lovelace.warning.entity_not_found",
            "entity",
            this._config.entity
          )}
        </hui-warning>
      `;

    const dir =
      c.dir ??
      this.hass.translationMetadata.translations[this.hass.language || "en"]
        .isRTL
        ? "rtl"
        : "ltr";

    const showSlider =
      c.stateObj.state !== "unavailable" &&
      c.hasSlider &&
      !(c.isOff && this._config.hide_when_off);
    const showToggle = this._config.toggle && c.hasToggle;
    const showValue = showToggle
      ? false
      : this._config.hide_state === false
      ? true
      : this._config.hide_state || this.hide_state
      ? false
      : c.isOff && this._config.hide_when_off
      ? false
      : true;

    const content = html`
      <div class="wrapper" @click=${(ev) => ev.stopPropagation()}>
        ${showSlider
          ? html`
              ${this._config.colorize && c.background
                ? html`
                    <style>
                      ha-slider.slider-entity-row.colorize::part(track) {
                        background: ${c.background};
                      }
                      ha-slider.slider-entity-row.colorize::part(indicator) {
                        background: transparent;
                      }
                    </style>
                  `
                : ""}
              <ha-slider
                .min=${c.min}
                .max=${c.max}
                .step=${c.step}
                .value=${c.value}
                .dir=${dir}
                labeled
                pin
                @change=${(ev) =>
                  (c.value = (
                    this.shadowRoot.querySelector("ha-slider") as any
                  ).value)}
                class=${`slider-entity-row${
                    this._config.full_row || this._config.grow ? " full" : ""
                  }${
                    this._config.colorize ? " colorize" : ""}`
                  }
                ignore-bar-touch
              ></ha-slider>
            `
          : ""}
        ${showToggle ? c.renderToggle(this.hass) : ""}
        ${showValue
          ? html`<span class="state">
              ${c.stateObj.state === "unavailable"
                ? this.hass.localize("state.default.unavailable")
                : c.string}
            </span>`
          : ""}
      </div>
    `;

    if (this._config.full_row)
      if (this._config.hide_when_off && c.isOff) return html``;
      else if (this._config.show_icon === true) {
        const conf = this._config as any;
        return html`
          <div class="wrapper">
            <state-badge
              .hass=${this.hass}
              .stateObj=${c.stateObj}
              .overrideIcon=${conf.icon}
              .overrideImage=${conf.image}
              .stateColor=${conf.state_color}
            ></state-badge>
            ${content}
          </div>
        `;
      } else return content;

    return html`
      <hui-generic-entity-row
        .hass=${this.hass}
        .config=${this._config}
        .catchInteraction=${false}
      >
        ${content}
      </hui-generic-entity-row>
    `;
  }

  static get styles() {
    return css`
      .wrapper {
        display: flex;
        align-items: center;
        justify-content: flex-end;
        flex: 7;
        height: 40px;
      }
      .state {
        min-width: var(--slider-entity-row-state-min-width, 45px);
        text-align: end;
        justify-content: flex-end;
        margin-left: 8px;
      }
      ha-entity-toggle {
        min-width: auto;
        margin-left: 8px;
      }
      ha-slider {
        width: 100%;
        min-width: 100px;
        --paper-slider-secondary-color: transparent;
      }
      ha-slider.slider-entity-row[size="small"] {
        --thumb-height: var(--slider-entity-row-thumb-size, var(--slider-entity-row-thumb-height, 16px));
        --thumb-width: var(--slider-entity-row-thumb-size, var(--slider-entity-row-thumb-width, 16px));
        --track-size: var(
          --slider-entity-row-track-size,
          var(--ha-slider-track-size, 4px)
        );
        padding: var(--slider-entity-row-slider-padding, 0 calc(var(--slider-entity-row-thumb-size, var(--slider-entity-row-thumb-width, 16px)) / 2));
      }
      ha-slider.slider-entity-row:not(.full) {
        max-width: 200px;
      }
      ha-slider.slider-entity-row::part(track) {
        background: var(--slider-entity-row-track-color, var(--ha-slider-track-color, var(--disabled-color)));
      }
      ha-slider.slider-entity-row::part(indicator) {
        background: var(--slider-entity-row-indicator-color, var(--ha-slider-indicator-color, var(--primary-color)));
      }
      ha-slider.slider-entity-row::part(thumb) {
        background: var(--slider-entity-row-thumb-color, var(--slider-entity-row-indicator-color, var(--ha-slider-thumb-color, var(--primary-color))));
        overflow: visible;
      }
      ha-slider.slider-entity-row::part(thumb)::before {
          content: "";
          border-radius: 50%;
          position: absolute;
          width: calc(var(--thumb-width) * 2 + 8px);
          height: calc(var(--thumb-height) * 2 + 8px);
          background-color: var(--slider-entity-row-thumb-color, var(--slider-entity-row-indicator-color, var(--ha-slider-thumb-color, var(--primary-color))));
          left: calc(-50% - 4px);
          top: calc(-50% - 4px);
          z-index: -1;
          opacity: 0;
      }
      ha-slider.slider-entity-row::part(thumb):hover::before {
          opacity: var(--slider-entity-row-thumb-hover-opacity, var(--ha-ripple-hover-opacity, 0.08));
      }
      ha-slider.slider-entity-row::part(thumb):active::before {
          opacity: var(--slider-entity-row-thumb-pressed-opacity, var(--ha-ripple-pressed-opacity, 0.12));
      }
      ha-slider.slider-entity-row::part(tooltip) {
        --wa-tooltip-content-color: var(--slider-entity-row-tooltip-color, var(--ha-tooltip-text-color, var(--primary-text-color)));
        --wa-tooltip-font-size: var(--slider-entity-row-tooltip-font-size, var(--ha-tooltip-font-size, var(--ha-font-size-s)));
        --wa-tooltip-font-weight: var(--slider-entity-row-tooltip-font-weight, var(--ha-tooltip-font-weight, var(--ha-font-weight-normal)));
        --wa-tooltip-background-color: var(--slider-entity-row-tooltip-background-color, var(--ha-tooltip-background-color, var(--secondary-background-color)));
        --wa-tooltip-border-radius: var(--slider-entity-row-tooltip-border-radius, var(--ha-tooltip-border-radius, var(--ha-border-radius-sm)));
        --wa-tooltip-border-width: var(--slider-entity-row-tooltip-border-width, 0px);
        --wa-tooltip-border-color: var(--slider-entity-row-tooltip-border-color, currentColor);
        --wa-tooltip-border-style: var(--slider-entity-row-tooltip-border-style, none);
      }
    `;
  }
}

if (!customElements.get("slider-entity-row")) {
  customElements.define("slider-entity-row", SliderEntityRow);
  console.groupCollapsed(
    `%c💡 SLIDER-ENTITY-ROW ${pjson.version} IS INSTALLED 💡`,
    "color: white; background-color: #CE3226; padding: 2px 5px; font-weight: bold; border-radius: 5px;",
    ""
  );
  console.log('Readme:', 'https://github.com/Lint-Free-Technology/lovelace-slider-entity-row');
  console.groupEnd();
}
