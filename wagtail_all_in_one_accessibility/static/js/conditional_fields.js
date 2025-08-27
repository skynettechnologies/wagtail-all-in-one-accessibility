(function() {
    function toggleWidgetPositionFields() {
        const enablePosition = document.querySelector('#id_enable_widget_icon_position');
        const show = enablePosition.checked;

        toggleField('.field-right-row', show);
        toggleField('.field-bottom-row', show);
        
        toggleField('.field-aioa-place', !show);
    }

    function toggleCustomSizeFields() {
        const enableCustomSize = document.querySelector('#id_enable_icon_custom_size');
        const show = enableCustomSize.checked;

        toggleField('.field-aioa-size-value', show);
        toggleField('.field-aioa-icon-size', !show);
    }

    function toggleField(selector, show) {
        const el = document.querySelector(selector);
        if (el) {
            el.style.display = show ? 'block' : 'none';
        }
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

        // Initialize on page load
        toggleWidgetPositionFields();
        toggleCustomSizeFields();
    }

    document.addEventListener('DOMContentLoaded', init);
})();
