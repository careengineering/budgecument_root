'use strict';

// Modal Operations
(function() {
    document.addEventListener('DOMContentLoaded', () => {
        // Event Delegation for Modals
        document.body.addEventListener('click', function(e) {
            const trigger = e.target.closest('[data-modal-target]');
            if (trigger) {
                const targetId = trigger.dataset.modalTarget;
                const modal = document.getElementById(targetId);
                const uid = trigger.dataset.uid;
                const text = trigger.dataset.modalText;
                const url = trigger.dataset.deleteUrl;

                if (modal) {
                    showModal(modal, { uid, text, url });
                }
            }
        });

        // Initialize Select2
        $('select').select2({
            theme: 'bootstrap-5',
            placeholder: "Lütfen seçim yapın",
            allowClear: true
        });

        // Initialize dynamic fields
        updateFieldVisibility();
        setupEventListeners();
    });

    function showModal(modalElement, { uid, text, url }) {
        const form = modalElement.querySelector('form');
        const textElement = modalElement.querySelector('.modal-text');
        const uidInput = modalElement.querySelector('[name="uid"]');

        if (form && textElement && uidInput) {
            textElement.textContent = text;
            form.action = url;
            uidInput.value = uid;
            new bootstrap.Modal(modalElement).show();
        }
    }

    // Dynamic Field Management
    function updateFieldVisibility() {
        const type = $('#id_transaction_type').val();
        $('.dynamic-field').removeClass('active');
        $(`.${type}-fields`).addClass('active');
    }

    function setupEventListeners() {
        // Transaction Type Change
        $('#id_transaction_type').on('change', function() {
            updateFieldVisibility();
            resetDependentFields();
        });

        // Source Account Change (with debounce)
        $('#id_source_account').on('change', _.debounce(function() {
            const sourceUid = this.value;
            const type = $('#id_transaction_type').val();
            
            if (type === 'transfer' && sourceUid) {
                loadDestinationAccounts(sourceUid);
            }
        }, 300));

        // Currency Symbol Update
        $('#id_source_account, #id_destination_account').on('change', function() {
            updateCurrencySymbol(this.value);
        });
    }

    function loadDestinationAccounts(sourceUid) {
        const urlTemplate = document.getElementById('destination-accounts-url').dataset.url;
        const url = urlTemplate.replace('00000000-0000-0000-0000-000000000000', sourceUid);
        const $destination = $('#id_destination_account');

        $.ajax({
            url: url,
            method: 'GET',
            beforeSend: () => {
                $destination.prop('disabled', true).html('<option value="">Yükleniyor...</option>');
            },
            success: (data) => {
                const options = data.length ? 
                    data.map(acc => `<option value="${acc.uid}" data-currency="${acc.currency__code}">${acc.name} (${acc.currency__code})</option>`) : 
                    ['<option value="">Uygun hesap bulunamadı</option>'];
                
                $destination.html(options.join('')).prop('disabled', false);
            },
            error: () => {
                $destination.html('<option value="">Hata oluştu</option>').prop('disabled', true);
            }
        });
    }

    function updateCurrencySymbol(accountId) {
        if (accountId) {
            const account = document.querySelector(`option[value="${accountId}"]`);
            if (account) {
                const currency = account.dataset.currency;
                document.querySelectorAll('.currency-symbol').forEach(el => {
                    el.textContent = currency;
                });
            }
        }
    }

    function resetDependentFields() {
        $('#id_destination_account').val(null).trigger('change');
        $('#id_source_account').val(null).trigger('change');
        updateCurrencySymbol('');
    }
})();