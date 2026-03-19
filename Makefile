librelane:
	nix-shell librelane --run "librelane config.yaml --pdk ihp-sg13cmos5l --pdk-root pdk --manual-pdk --overwrite --run-tag spm_chip"

.PHONY: librelane