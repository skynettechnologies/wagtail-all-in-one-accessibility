(function () {

    function toggleWidgetPositionFields() {
        const enablePosition = document.querySelector('#id_enable_widget_icon_position');
        if (!enablePosition) return;

        const show = enablePosition.checked;

        // Reset values when DISABLED
        if (!show) {
            setValue('#id_to_the_right_px', 20);
            setValue('#id_to_the_right', 'to_the_left');
            setValue('#id_to_the_bottom_px', 20);
            setValue('#id_to_the_bottom', 'to_the_bottom');
        }

        toggleField('.field-right-row', show);
        toggleField('.field-bottom-row', show);
        toggleField('.field-aioa-place', !show);
    }

    function toggleCustomSizeFields() {
        const enableCustomSize = document.querySelector('#id_enable_icon_custom_size');
        if (!enableCustomSize) return;

        const show = enableCustomSize.checked;

        // Reset values when DISABLED
        if (!show) {
            setValue('#id_aioa_size_value', 50);
            setValue('#id_aioa_icon_size', 'aioa-default-icon');
        }

        toggleField('.field-aioa-size-value', show);
        toggleField('.field-aioa-icon-size', !show);
    }

    function toggleField(selector, show) {
        const el = document.querySelector(selector);
        if (el) {
            el.style.display = show ? 'block' : 'none';
        }
    }

    function setValue(selector, value) {
        const el = document.querySelector(selector);
        if (!el) return;

        el.value = value;

        // Important for Wagtail/Django change detection
        el.dispatchEvent(new Event('change', { bubbles: true }));
    }

    function init() {
        const widgetToggle = document.querySelector('#id_enable_widget_icon_position');
        const customSizeToggle = document.querySelector('#id_enable_icon_custom_size');

        if (widgetToggle) {
            widgetToggle.addEventListener('change', toggleWidgetPositionFields);
        }

        if (customSizeToggle) {
            customSizeToggle.addEventListener('change', toggleCustomSizeFields);
        }

        toggleWidgetPositionFields();
        toggleCustomSizeFields();
    }

    document.addEventListener('DOMContentLoaded', init);
})();
