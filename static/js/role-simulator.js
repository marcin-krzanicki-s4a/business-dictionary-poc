// Advanced Role-Based Access Simulation
document.addEventListener('DOMContentLoaded', function() {
    const roleBtns = document.querySelectorAll('.role-filter-btn');
    const attributeRows = document.querySelectorAll('.attribute-row');
    const actionRows = document.querySelectorAll('.action-row');
    const attributesInfo = document.getElementById('attributes-info');
    const actionsInfo = document.getElementById('actions-info');

    if (roleBtns.length === 0) return;

    // Parse condition string to check if it matches current role/position
    function checkCondition(conditionStr, selectedRole) {
        if (!conditionStr) return true; // No condition = visible to all
        
        // Replace condition variables with actual values
        // Simulate different positions for different roles
        let position = selectedRole;
        if (selectedRole === 'Captain') position = 'Captain';
        if (selectedRole === 'First Officer') position = 'First Officer';
        if (selectedRole === 'Pilot') position = 'Pilot';
        if (selectedRole === 'Flight Attendant') position = 'Flight Attendant';
        if (selectedRole === 'Ops Manager') position = 'Manager';
        if (selectedRole === 'Dispatcher') position = 'Dispatcher';

        // Simple condition evaluation
        let condition = conditionStr
            .replace(/userRole\s*==\s*['"]([^'"]+)['"]/g, `"${selectedRole}" == "$1"`)
            .replace(/position\s*==\s*['"]([^'"]+)['"]/g, `"${position}" == "$1"`)
            .replace(/userRole\s*==\s*['"]([^'"]+)['"]/g, selectedRole === '$1' ? 'true' : 'false')
            .replace(/position\s*==\s*['"]([^'"]+)['"]/g, position === '$1' ? 'true' : 'false');

        // Handle 'or' conditions
        if (conditionStr.includes('or')) {
            const parts = conditionStr.split('or').map(p => p.trim());
            return parts.some(part => checkConditionPart(part, selectedRole, position));
        }

        return checkConditionPart(conditionStr, selectedRole, position);
    }

    function checkConditionPart(part, selectedRole, position) {
        // Check role condition
        if (part.includes("userRole")) {
            const roleMatch = part.match(/['"]([^'"]+)['"]/);
            if (roleMatch && roleMatch[1] === selectedRole) {
                return true;
            }
            return part.includes(selectedRole);
        }
        
        // Check position condition
        if (part.includes("position")) {
            const positionMatch = part.match(/['"]([^'"]+)['"]/);
            if (positionMatch && positionMatch[1] === position) {
                return true;
            }
            return part.includes(position);
        }

        return true;
    }

    // Set up role button click handlers
    roleBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            const selectedRole = this.dataset.role;
            
            // Update active button
            roleBtns.forEach(b => b.classList.remove('uk-button-primary'));
            this.classList.add('uk-button-primary');

            // If "All Roles" selected, show everything
            if (selectedRole === 'all') {
                attributeRows.forEach(row => {
                    row.style.display = '';
                });

                actionRows.forEach(row => {
                    row.style.display = '';
                });

                if (attributesInfo) {
                    attributesInfo.textContent = 'Showing all attributes (all roles)';
                }
                if (actionsInfo) {
                    actionsInfo.textContent = 'Showing all actions (all roles)';
                }
                return;
            }

            // Filter attributes
            let visibleAttributeCount = 0;
            attributeRows.forEach(row => {
                const condition = row.dataset.condition;
                const isVisible = checkCondition(condition, selectedRole);
                
                if (isVisible) {
                    row.style.display = '';
                    visibleAttributeCount++;
                } else {
                    row.style.display = 'none';
                }
            });

            // Filter actions
            let visibleActionCount = 0;
            actionRows.forEach(row => {
                const condition = row.dataset.condition;
                const isVisible = checkCondition(condition, selectedRole);
                
                if (isVisible) {
                    row.style.display = '';
                    visibleActionCount++;
                } else {
                    row.style.display = 'none';
                }
            });

            // Update info text
            if (attributesInfo) {
                attributesInfo.textContent = `Showing ${visibleAttributeCount} attribute(s) for role: ${selectedRole}`;
            }
            if (actionsInfo) {
                actionsInfo.textContent = `Showing ${visibleActionCount} action(s) for role: ${selectedRole}`;
            }
        });
    });

    // Make "All Roles" button active by default
    const allRolesBtn = document.querySelector('.role-filter-all');
    if (allRolesBtn) {
        allRolesBtn.classList.add('uk-button-primary');
        allRolesBtn.click();
    } else if (roleBtns.length > 0) {
        roleBtns[0].classList.add('uk-button-primary');
        roleBtns[0].click();
    }

    console.log('Advanced role-based access simulation initialized');
});
