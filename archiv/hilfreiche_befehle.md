# Hilfreiche Befehle

### DEVELOP ➡️ ALLE BRANCHES

```bash
# Sicherstellen, dass develop aktuell ist
git checkout develop
git pull origin develop

# Liste der Branches, die du überschreiben willst
branches=("feature/abakan" "feature/angeles" "feature/berlin" "refactor/full-restructure")

# Für jede Branch hart resetten
for branch in "${branches[@]}"; do
    echo "🔄 Wechsle zu $branch..."
    git checkout "$branch"

    echo "🚨 Mache harten Reset auf develop..."
    git reset --hard develop

    echo "📤 Push mit force..."
    git push origin "$branch" --force
done

# Zurück zu develop
git checkout develop
```

### DEVELOP ➡️ EIN BRANCH

```bash
# Stelle sicher, dass du auf develop bist und alles aktuell ist
git checkout develop
git pull origin develop

# Wechsle zu main
git checkout main

# Harte Übernahme von develop
git reset --hard develop

# Push mit Force
git push origin main --force
```