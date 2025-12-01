# formation-python-filerouge

Formation Python & DevOps (73h) - Projet fil rouge : application d'alertes pour la Guadeloupe. 14 modules du débutant au déploiement CI/CD automatisé.

## Infrastructure

Ce projet utilise Terraform pour gérer le dépôt GitHub.

### Prérequis

- [Terraform](https://www.terraform.io/) >= 1.0
- Un token GitHub avec les permissions nécessaires

- [direnv](https://direnv.net/) pour la gestion des variables d'environnement
- [pass](https://www.passwordstore.org/) pour le stockage sécurisé du token


### Configuration


1. Initialiser Terraform :
   ```bash
   cd terraform
   terraform init
   ```


### Déploiement

```bash
cd terraform
terraform plan
terraform apply
```

## Licence

MIT
