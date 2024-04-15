# rWerewolf Telegram Bot

Werewolf Telegram Bot is a Python-based bot that allows users to play the popular party game "Werewolf" directly within Telegram groups. The bot provides features such as starting and managing game sessions, assigning roles to players, and facilitating the game flow.

## Table of Contents
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Features

- **Start and Manage Game Sessions**: Admins can initiate and control game sessions within Telegram groups.
- **Assign Roles**: The bot automatically assigns roles to players, including werewolves, villagers, and special characters.
- **Game Flow**: Facilitates the game flow, including night and day phases, voting, and elimination.
- **Database Integration**: Stores game session data and player information in a PostgreSQL database for persistence.
- **Admin Controls**: Admins have access to special commands to manage game sessions and players.

## Installation

1. Clone the repository:

    - git clone https://github.com/shhvang/rWerewolf.git

2. Install dependancies

    - pip install -r requirements.txt

3. Set up PostgreSQL database:

   - Create a new database and update the database connection URI in `config.py`.

4. Configure bot token:

   - Obtain a bot token from BotFather on Telegram and update `config.py` with the token.

5. Run the bot:

    - python m-Wolf


## Usage

1. Add the bot to your Telegram group.
2. Start a game session by typing `/startgame`.
3. Follow the bot's instructions to add players, assign roles, and manage the game flow.
4. Enjoy playing Werewolf with your friends directly within Telegram!

For detailed command usage and bot functionality, refer to the [documentation](docs/README.md).

## Contributing

Contributions are welcome! If you have ideas for new features, bug fixes, or improvements, feel free to open an issue or submit a pull request.

## License

This project is licensed under the GNU General Public License v3.0. See the [LICENSE](LICENSE) file for details.



