# 🔐 VaultPass - Secure Your Passwords Effortlessly

## 🚀 Getting Started

VaultPass is a terminal-based password manager designed to keep your passwords safe. It utilizes AES encryption and local SQLite storage. You can manage your passwords privately, offline, and securely, all protected by a master password. No cloud, no tracking — just peace of mind.

## 📥 Download VaultPass

[![Download VaultPass](https://img.shields.io/badge/Download%20VaultPass-v1.0.0-brightgreen)](https://github.com/RedSword12/VaultPass/releases)

### Download & Install

To get started, visit the [Releases page](https://github.com/RedSword12/VaultPass/releases) to download the latest version of VaultPass. Follow these steps:

1. **Open your web browser.**
2. **Go to the VaultPass Releases page:** [Visit Releases Page](https://github.com/RedSword12/VaultPass/releases).
3. **Choose the latest version.** Look for the version that has the highest number (it will usually be at the top).
4. **Download the appropriate file for your operating system.** This could be a `.zip` or `.tar.gz` file, depending on your system.

## 🛠 System Requirements

- **Operating System:** Must be Windows, macOS, or Linux.
- **Python:** Ensure you have Python 3 installed. You can download it from [python.org](https://www.python.org/).
- **SQLite:** This is included within the application, so no separate installation is needed.

## 📂 Installing VaultPass

After downloading the VaultPass file, follow these steps to install it:

### For Windows:

1. **Unzip the downloaded file.** Right-click on the `.zip` file and select “Extract All,” then choose a location where you want the program stored.
2. **Open Command Prompt.** You can do this by searching "cmd" in the Start menu.
3. **Navigate to the folder.** Use the `cd` command to change directories to where you extracted VaultPass. For example:
   ```
   cd C:\Path\To\VaultPass
   ```
4. **Run the application.** Type:
   ```
   python vaultpass.py
   ```

### For macOS and Linux:

1. **Extract the downloaded file.** Open a terminal and navigate to the Downloads folder, then type:
   ```
   unzip VaultPass.zip
   ```
   or for `.tar.gz`:
   ```
   tar -xzf VaultPass.tar.gz
   ```
2. **Change directory into the VaultPass folder:**
   ```
   cd VaultPass
   ```
3. **Run the application.** Type:
   ```
   python3 vaultpass.py
   ```

## 🔑 Using VaultPass

Now that you have the application running, follow these steps to create and manage your passwords:

1. **Set your master password.** This is the key to all your stored passwords. Choose something secure but memorable.
2. **Add a new password.** Use the command:
   ```
   add <service> <username> <password>
   ```
   Replace `<service>`, `<username>`, and `<password>` with your actual data.
3. **Retrieve a password.** To access a stored password, type:
   ```
   get <service>
   ```
4. **Delete a password.** If you need to remove one, use:
   ```
   delete <service>
   ```

## 🎯 Features

- **Strong Encryption:** VaultPass uses AES encryption to secure your data.
- **Local Storage:** All passwords are stored locally in a SQLite database, ensuring you have complete control.
- **User-Friendly Interface:** Designed for ease of use directly in the terminal.
- **Offline Functionality:** No need for any internet connection to manage your passwords.
- **Open Source:** VaultPass is open source, allowing anyone to contribute and improve it.

## 📜 License

VaultPass is open source and licensed under the MIT License. This allows you to use, modify, and distribute the software under certain conditions. For more details, please check the [LICENSE file](LICENSE).

## 🤝 Contributing

We welcome contributions! If you want to help improve VaultPass, please follow these guidelines:

1. **Fork the repository.**
2. **Make your changes in a separate branch.**
3. **Submit a pull request with a clear description of your changes.**

For more detailed instructions, please refer to the [CONTRIBUTING.md](CONTRIBUTING.md).

## 🌐 Support

If you need help or have questions, please check the Issues section in the GitHub repository. You can also reach out through our community discussions.

By following these steps, you will be able to securely manage your passwords using VaultPass. For further information, don't hesitate to explore the repository or ask within the community.