# -*- mode: ruby -*-
# vi: set ft=ruby :

VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  config.vm.box = "bento/ubuntu-16.04"

  config.vm.define "nanotoms" do |nanotoms|
  end

  config.vm.network "forwarded_port", guest: 8000, host: 8000
  config.vm.network "forwarded_port", guest: 5432, host: 5432
  config.vm.network "forwarded_port", guest: 7474, host: 7474
  config.vm.network "forwarded_port", guest: 7687, host: 7687

  config.vm.network "private_network", ip: "192.168.20.17"

  config.vm.provider "virtualbox" do |provider|
    provider.customize ["modifyvm", :id, "--memory", "2048"]
    provider.name = "nanotoms"
  end

  config.vm.provision "ansible" do |ansible|
    ansible.playbook = ".vagrant_provisioning/playbook.yml"
    # ansible.tags = ""
    # ansible.verbose = "vvv"
  end
end
