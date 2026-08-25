(function () {
    function toggleWidgetPositionFields() {
        const enablePosition = document.querySelector(
            '#id_enable_widget_icon_position'
        );

        if (!enablePosition) {
            return;
        }

        const show = enablePosition.checked;

        // Reset values when disabled
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
        const enableCustomSize = document.querySelector(
            '#id_enable_icon_custom_size'
        );

        if (!enableCustomSize) {
            return;
        }

        const show = enableCustomSize.checked;

        // Reset values when disabled
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

        if (!el) {
            return;
        }

        el.value = value;

        // Important for Wagtail/Django change detection
        el.dispatchEvent(
            new Event('change', {
                bubbles: true
            })
        );
    }

    function insertNoticeBanner() {
        // Prevent duplicate insertion
        if (document.querySelector('#aioa-notice-banner')) {
            return;
        }

        // Find the Hex Color Code input
        const anchor = document.querySelector('#id_aioa_color_code');

        if (!anchor) {
            return;
        }

        /*
         * Find the label associated with the Hex Color Code input.
         * We use the label and input together to locate the complete
         * field section, including:
         *
         * - Hex Color Code heading
         * - Help text
         * - Input field
         */
        const label = document.querySelector(
            'label[for="id_aioa_color_code"]'
        );

        let fieldContainer = null;

        /*
         * Find the smallest common parent containing both
         * the label and the input.
         */
        if (label) {
            let current = label.parentElement;

            while (current) {
                if (current.contains(anchor)) {
                    fieldContainer = current;
                    break;
                }

                current = current.parentElement;
            }
        }

        /*
         * Fallback selectors for different Wagtail versions.
         */
        if (!fieldContainer) {
            fieldContainer =
                anchor.closest('[data-field-wrapper]') ||
                anchor.closest('.w-field') ||
                anchor.closest('.field') ||
                anchor.closest('li') ||
                anchor.closest('.w-field__wrapper') ||
                anchor.parentElement;
        }

        if (!fieldContainer) {
            return;
        }

        const noticeHTML = `
            <div id="aioa-notice-banner">
                <p
                    style="
                        margin: 0 0 6px 0;
                        color: inherit;
                        font-size: 0.9rem;
                        line-height: 1.55;
                    "
                >
                    <strong>NOTE:</strong>
                    Currently, All in One Accessibility is dedicated to enhancing
                    accessibility specifically for websites and online stores.
                    Please upgrade to the full version of
                    <a
                        href="https://ada.skynettechnologies.us/trial-subscription"
                        target="_blank"
                        style="
                            color: #9b6dff;
                            font-weight: 600;
                            text-decoration: underline;
                        "
                    >
                        All in One Accessibility Pro with 10 days free trial
                    </a>.
                </p>

                <p
                    style="
                        margin: 0 0 16px 0;
                        color: inherit;
                        font-size: 0.9rem;
                        line-height: 1.55;
                        opacity: 0.85;
                    "
                >
                    It may take a few seconds for changes to appear on your website.
                    If you don't see the changes, try clearing your browser cache
                    or checking in a private browsing window.
                </p>
            </div>
        `;

        /*
         * Insert the NOTE before the complete Hex Color Code section.
         *
         * This places the NOTE before:
         * - Hex Color Code heading
         * - Help text
         * - Color input
         */
        fieldContainer.insertAdjacentHTML(
            'beforebegin',
            noticeHTML
        );
    }

    function init() {
        const widgetToggle = document.querySelector(
            '#id_enable_widget_icon_position'
        );

        const customSizeToggle = document.querySelector(
            '#id_enable_icon_custom_size'
        );

        if (widgetToggle) {
            widgetToggle.addEventListener(
                'change',
                toggleWidgetPositionFields
            );
        }

        if (customSizeToggle) {
            customSizeToggle.addEventListener(
                'change',
                toggleCustomSizeFields
            );
        }

        // Initialize field visibility
        toggleWidgetPositionFields();
        toggleCustomSizeFields();

        // Insert the NOTE above the complete Hex Color Code section
        try {
            insertNoticeBanner();
        } catch (error) {
            console.error(
                'AIOA: Error inserting notice banner:',
                error
            );
        }
    }

    document.addEventListener(
        'DOMContentLoaded',
        init
    );
})();