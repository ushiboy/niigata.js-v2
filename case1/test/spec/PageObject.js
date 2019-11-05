const {By, Key, until} = require('selenium-webdriver');

export class FishList {

  constructor(driver) {
    this.driver = driver;
  }

  async open() {
    await this.driver.get('http://localhost:8080');
    return this;
  }

  async waitForRowToFinishLoading() {
    await this.driver.wait(async () => {
      const rows = await this.getRows();
      return rows.length !== 0;
    }, 5000);
    return this;
  }

  async clickSelect() {
    await this.driver.findElement(By.id('select-button')).click();
    return this.driver.switchTo().alert();
  }

  async clickAllCheck() {
    const check = await this.driver.findElement(By.id('all-check'));
    check.click();
    return this;
  }

  async getRows() {
    const rows = await this.driver.findElement(By.id('fish-list')).findElements(By.tagName('tr'));
    return rows.map(r => {
      return new FishListRow(this.driver, r);
    });
  }
}

export class FishListRow {

  constructor(driver, el) {
    this._driver = driver;
    this._el = el;
  }

  async getName() {
    const cols = await this._el.findElements(By.tagName('td'));
    return cols[1].getText();
  }

  async clickCheckBox() {
    await this._el.findElement(By.className('select-row')).click();
    return this;
  }

}
