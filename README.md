# Visual Studio Code Language Packs

Visual Studio Code is localized into many different languages using Language Pack extensions. Language Packs can be installed from the [Visual Studio Code Marketplace](https://marketplace.visualstudio.com/search?target=VSCode&category=Language%20Packs&sortBy=Installs), or from the `Configure Display Language` command in the Command Palette. VS Code can also recommend a matching Language Pack based on the operating system's display language.

The original English strings can be found in the source code of the [open source repository](https://github.com/microsoft/vscode), and the localized strings for supported languages can be found in this repository.

Localized resource files are managed and edited through the Microsoft Localization Platform. Updated resources are exported to this repository before language packs are published.

## Supported language packs

This repository currently contains 14 Language Packs for Visual Studio Code.

|Language|Visual Studio Code Language ID|MLCP Language Code|
|--------|--------|--------|
|**French**|fr|French (fr-fr)|
|**Italian**|it|Italian (it-it)|
|**German**|de|German (de-de)|
|**Spanish**|es|Spanish (es-es)|
|**Russian**|ru|Russian (ru-ru)|
|**Chinese (Simplified)**|zh-cn|Chinese Simplified (zh-cn)|
|**Chinese (Traditional)**|zh-tw|Chinese Traditional (zh-tw)|
|**Japanese**|ja|Japanese (ja-jp)|
|**Korean**|ko|Korean (ko-kr)|
|**Czech**|cs|Czech (cs-CZ)|
|**Portuguese (Brazil)**|pt-br|Portuguese (Brazil) (pt-br)|
|**Turkish**|tr|Turkish (tr-tr)|
|**Polish**|pl|Polish (pl-pl)|
|**Pseudo Language**|qps-ploc|Pseudo (qps-ploc)|

## Repository layout and publishing

Each `i18n/vscode-language-pack-*` directory is an independently packaged VS Code extension. Its `package.json` declares the supported VS Code version and the translation resources contributed by the package.

GitHub Actions packages every Language Pack on pushes and pull requests to `main`. The release pipeline publishes a selected pack on its weekly schedule or when manually configured with the `languagePack` pipeline variable. Translation resources are machine-generated exports from the Microsoft Localization Platform; do not edit them directly.

## Contributing

If you want to give feedback or report an issue with a translation, please [create an issue](https://github.com/microsoft/vscode-loc/issues/new) after checking whether it has already been reported.

Translation strings are managed on the Microsoft Localization Platform, and changes to strings can only be made there. Consequently, pull requests fixing translations are not accepted. Pull requests for repository metadata, documentation, and build configuration are reviewed at the maintainers' discretion.

## Legal

Before we can accept your pull request, you will need to sign a **Contribution License Agreement**. All you need to do is submit a pull request. It will then be appropriately labeled (e.g., `cla-required`, `cla-norequired`, `cla-signed`, `cla-already-signed`). If you already signed the agreement, we will continue with reviewing the PR; otherwise, our system will tell you how you can sign the CLA. Once you sign the CLA, all future PRs will be labeled as `cla-signed`.

# Microsoft Open Source Code of Conduct

This project has adopted the [**Microsoft Open Source Code of Conduct**](https://opensource.microsoft.com/codeofconduct/).
For more information, see the [**Code of Conduct FAQ**](https://opensource.microsoft.com/codeofconduct/faq/) or contact [**opencode@microsoft.com**](mailto:opencode@microsoft.com) with any additional questions or comments.

## License

[MIT](LICENSE.md)
