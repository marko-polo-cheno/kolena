---
icon: kolena/help-16
hide:
  - navigation
  - toc
---

# :kolena-help-20: Frequently Asked Questions

This page answers common questions about using Kolena to test ML models.

If you don't see your question here, please reach out to us on Slack or at
[contact@kolena.io](mailto:contact@kolena.io)!

??? question "How do I generate an API token?"

    Generate an API token by visiting [app.kolena.io/~/developer](https://app.kolena.io/redirect/developer), on the
    bottom of the lefthand sidebar, then copy/paste the shell snippet to set this token as `KOLENA_TOKEN` in your
    environment.

??? question "How many API tokens can I generate?"

    API tokens are scoped to your username. Each user is limited to one valid token at a time — generating a new
    token from [app.kolena.io/~/developer](https://app.kolena.io/redirect/developer) invalidates any previous token
    generated for your user.

    To retrieve a service user API token that is not scoped to a specific username, please reach out to us on Slack or
    at [contact@kolena.io](mailto:contact@kolena.io).

??? question "How can I add new users to my organization?"

    Certain members of each organization have administrator privileges. These administrators can add new users, and
    grant users administrator privileges, by visiting
    [app.kolena.io/~/organization](https://app.kolena.io/redirect/organization) and adding entries to the **Authorized
    Users** table.

??? question "What data types does Kolena support?"

    Testing in Kolena is fully customizable and supports computer vision, natural language processing, and structured
    data (tabular, time series) machine learning models. This includes images, documents, videos, 3D models and point
    clouds, and more.

    See the available data types in [`kolena.workflow.TestSample`][kolena.workflow.TestSample], and the available
    annotation types in [`kolena.workflow.annotation`][kolena.workflow.annotation.Annotation].

    We're constantly adding new data types and annotation types — if you don't see what you're looking for, reach out
    to us and we'll happily extend our system to support your use case.

??? question "I'm new to Kolena — how can I learn more about the platform and how to use it?"

    On each page, there is a button with the :kolena-learning-16: icon next to the page title. Click on this
    button to bring up a detailed tutorial explaining the contents of the current page and how it's used.

??? question "Do I have to upload my datasets to Kolena?"

    No. Kolena doesn't store your data (images, videos, documents, 3D assetes, etc.) directly, only URLs pointing to
    the right location in a cloud bucket or internal infrastructure that you own.

    While onboarding your team, we'll discuss what access restrictions are necessary for your data and select the right
    integration solution. As one example, as a part of the integration we might restrict access to files registered with
    Kolena to only users on your corporate VPN.

    We support a variety of integration patterns depending on your organization's requirements and security stance.
    [Get in touch with us to discuss details](https://www.kolena.io/schedule-a-demo)!

??? question "Do I have to upload my models to Kolena?"

    No. Tests are always run in your environment using the [`kolena` Python client](/using-kolena-client), and you never
    have to package or upload models to Kolena.

??? question "Where does Kolena fit into the MLOps development life cycle?"

    Kolena is primarily a testing (or "offline evaluation") platform, coming _after_ training and _before_ deployment.
    We believe that increased emphasis on this offline evaluation segment of the model development life cycle can save
    effort upstream in the data collection and training process as well as prevent headaches downstream in deployment.

??? question "How can I report a bug?"

    If you encounter a bug when using the `kolena` Python client or when using [app.kolena.io](https://app.kolena.io),
    message us on Slack, email your support representative or [contact@kolena.io](mailto:contact@kolena.io), or
    [open an issue on the `kolena` repository](https://github.com/kolenaIO/kolena/issues) for Python-client-related
    issues.

    Please include any relevant stacktrace or platform URL when reporting an issue.