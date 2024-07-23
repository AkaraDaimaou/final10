import React from 'react';

function Confirmation() {
    return (
        <div>
            <h2>Confirmation</h2>
            <p>Your registration was successful!</p>
            <a href="{{ .SiteURL }}/confirm-signup?confirmation_url={{ .ConfirmationURL }}"
  >Confirm your signup
</a>

        </div>
    );
}

export default Confirmation;
